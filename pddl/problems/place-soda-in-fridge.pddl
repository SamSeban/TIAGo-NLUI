(define (problem put_object_in_fridge) (:domain tiago_robot)
    (:objects
        soda - object
        fridge - location
        fridge_door - door
        robot_initial_location - location
    )

    (:init
        (at-robot robot_initial_location)
        (holding soda) ; Assuming the robot starts by holding the soda
        (door-location fridge_door fridge)
        (door-state fridge_door closed) ; Fridge is initially closed
        (hand-empty) ; This would be contradicted by (holding soda)
    )

    (:goal
        (and
            (at soda fridge)
         	(door-state fridge_door closed)
        )
    )
)
