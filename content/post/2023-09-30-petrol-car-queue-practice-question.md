---
title: petrol car queue question
date: 1970-09-30
draft: false
unlisted: true
---
okay



## Question 

There is a queue of N cars waiting at the filling station. 3 fuel dispensers, x, y, z. When a car arrives at front of the queue, driver can choose to go to any dispenser not occupied. If all unoccupied dispensers have less than required by the driver he has to wait. if more than one dispenser has the required liter, the driver chooses the one labeled with the smallest letter.Calculate max amount of waiting time.

Assume taking one liter of fuel takes exactly one second? example A[2,8,4,3,2], x= 7, y=11, z=3, then cars will be waiting 0, 0, 2, 2, 8 seconds.red liter, the driver chooses the one labeled with the smallest letter.

So the max waiting time is 8 from [0,0,2,2,8] in this example.

And if the car at the front of the queue has no match, then the answer ought to be -1. 

A pump must have all the gas required by a given car.

## Okay heres what I have 

```python
from collections import OrderedDict
from copy import deepcopy


def choose(needs, pumps):
    occupied = False
    for name, pump in pumps.items():
        if not pump["car"]:
            if needs <= pump["has"]:
                return name
        else:
            occupied = True

    # if all pumps are free but no choice was made, then we will never finish
    if not occupied:
        return -1


def init_pumps(input_pumps):
    """
    Example:
    >>> init_pumps({"x": 2, "y": 4})
    {
        "x": {"car": None, "has": 2},
        "y": {"car": None, "has": 4},
    }
    """
    pumps = OrderedDict()
    for name in sorted(input_pumps.keys()):
        pumps[name] = {"car": None, "has": input_pumps[name]}
    return pumps


def init_queue(input_queue):
    """
    Example
    >>> init_queue([1, 2])
    [{"needs": 1, "waits": 0}, {"needs": 2, "waits": 0}]
    """
    return [
        {"needs": x, "waits": 0}
        for x in input_queue
    ]


def dispense(pumps):
    for name, pump in pumps.items():
        car = pump["car"]
        if car:
            car["needs"] -= 1
            if car["needs"] == 0:
                pump["car"] = None
            pump["has"] -= 1


def assign(car, pump):
    assert not pump["car"]
    pump["car"] = car


def main():
    cases = [
        {
            "pumps": {"x": 7, "y": 11, "z": 3},
            "queue": [2, 8, 4, 3, 2],
        },
        {
            "pumps": {"x": 7, "y": 11, "z": 3},
            "queue": [2, 8, 4, 3, 2, 6],
        },
        {
            "pumps": {"x": 100, "y": 11, "z": 3},
            "queue": [9, 9, 9, 9, 9, 9],
        },
    ]
    for i, parameters in enumerate(cases):
        print("\n==================")
        print("case ", i, "parameters", parameters)
        time, finished_waiting = run(parameters)
        print("finished_waiting", finished_waiting)
        print("max wait time", time)
    print("Done, bye")


def wait(queue):
    for car in queue:
        car["waits"] += 1


def run(parameters):
    time = 0
    queue = init_queue(parameters["queue"])
    pumps = init_pumps(parameters["pumps"])
    finished_waiting = []
    assigning = True
    while queue:
        while assigning and queue:
            car = queue[0]
            choice = choose(car["needs"], pumps)
            if not choice:
                assigning = False
            elif choice == -1:
                print("uh oh, not enough gas. Quitting")
                return -1, finished_waiting
            else:
                queue.pop(0)
                finished_waiting.append(deepcopy(car))
                assign(car, pumps[choice])
        wait(queue)

        dispense(pumps)
        assigning = True
        if not queue:
            break
        time += 1
    return time, finished_waiting


if __name__ == "__main__":
    main()

```
