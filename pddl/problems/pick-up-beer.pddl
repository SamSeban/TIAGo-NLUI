(define (problem pick_up_beer) (:domain tiago_robot)
    (:objects
        beer - object
        fridge_door - door
        opener1 - object
        robot_initial_location fridge_location my_location - location
    )

    (:init
        (at-robot robot_initial_location)
        (hand-empty)
        (at beer fridge_location)
        (door-location fridge_door fridge_location)
        (door-state fridge_door closed)
    )

    (:goal
        (and
            (holding beer)
         	(door-state fridge_door closed)
            (at-robot my_location)
        )
    )
)
