# src/ai_controller.py
"""
Simple adaptive controller for the Pygame traffic simulator.

Algorithm:
 - Read queue lengths for each direction (number of vehicles whose x/y is
   <= stop line and not crossed).
 - Compute normalized weights for each direction.
 - Allocate green time proportional to weights, bounded by min/max.
 - Smooth allocation using exponential moving average to avoid large jumps.

This module exposes `start_controller(shared_state)` function which runs
a daemon thread and updates shared_state['defaultGreen'] in-place.
"""

import threading
import time
import numpy as np

def compute_queue_lengths(vehicles, stopLines, directionNumbers):
    q = [0,0,0,0]
    for dir_idx, dir_name in directionNumbers.items():
        lanes = vehicles.get(dir_name, {})
        cnt = 0
        for lane_idx in [0,1,2]:
            lane_list = lanes.get(lane_idx, [])
            for v in lane_list:
                try:
                    if getattr(v, 'crossed', 0) == 0:
                        if dir_name == 'right':
                            if getattr(v, 'x', 0) + v.image.get_rect().width >= stopLines[dir_name] - 5:
                                cnt += 1
                        elif dir_name == 'left':
                            if getattr(v, 'x', 0) <= stopLines[dir_name] + 5:
                                cnt += 1
                        elif dir_name == 'down':
                            if getattr(v, 'y', 0) + v.image.get_rect().height >= stopLines[dir_name] - 5:
                                cnt += 1
                        elif dir_name == 'up':
                            if getattr(v, 'y', 0) <= stopLines[dir_name] + 5:
                                cnt += 1
                except Exception:
                    pass
        q[dir_idx] = cnt
    return q

def start_controller(shared_state,
                     control_interval=2.0,
                     min_green=6,
                     max_green=45,
                     smoothing_alpha=0.6):
    thread = threading.Thread(target=_controller_loop,
                              args=(shared_state, control_interval, min_green, max_green, smoothing_alpha),
                              name="AIController")
    thread.daemon = True
    thread.start()
    return thread

def _controller_loop(shared_state, control_interval, min_green, max_green, alpha):
    directionNumbers = shared_state.get('directionNumbers', {0:'right',1:'down',2:'left',3:'up'})
    stopLines = shared_state.get('stopLines')
    vehicles = shared_state.get('vehicles')
    if stopLines is None or vehicles is None:
        print("[AI] Missing stopLines or vehicles in shared_state; controller exiting.")
        return

    defaultGreen = shared_state.get('defaultGreen', {0:20,1:20,2:20,3:20})
    smoothed = np.array([defaultGreen.get(i,20) for i in range(4)], dtype=float)

    while True:
        try:
            q = compute_queue_lengths(vehicles, stopLines, directionNumbers)
            q_arr = np.array(q, dtype=float)
            total = q_arr.sum()
            if total <= 0:
                weights = np.ones(4) / 4.0
            else:
                weights = q_arr / (total + 1e-8)

            base_cycle = 4 * min_green
            extra = min( max_green*4 - base_cycle, 5 * total )
            cycle_budget = base_cycle + extra
            candidate = weights * cycle_budget
            candidate = np.clip(candidate, min_green, max_green)
            candidate = candidate / (candidate.sum() + 1e-8) * cycle_budget

            smoothed = alpha * candidate + (1.0 - alpha) * smoothed

            for i in range(4):
                shared_state['defaultGreen'][i] = int(max(min_green, min(int(smoothed[i]), max_green)))

        except Exception as e:
            print("[AI] Exception in controller loop:", e)
        time.sleep(control_interval)