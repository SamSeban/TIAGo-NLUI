(define (domain tiago_robot)
    (:requirements :strips :typing)
    (:types
        object
        location
        door container - object
        state
    )

    (:constants
        open closed - state
    )

    (:predicates
        (at-robot ?loc - location)
        (hand-empty)
        (holding ?obj - object)
        (at ?obj - object ?loc - location)
        (door-state ?door - door ?state - state)
        (container-state ?container - container ?state - state)
        (door-location ?door - door ?loc - location)
        (can-open ?tool - object ?target - object)
        (empty ?container - container)
        (full ?container - container)
    )

    (:action navigate
        :parameters (?from - location ?to - location)
        :precondition (at-robot ?from)
        :effect (and
                    (not (at-robot ?from))
                    (at-robot ?to)
                )
    )
    (:action open_door
        :parameters (?door - door ?loc - location)
        :precondition (and
                        (at-robot ?loc)
                        (door-state ?door closed)
                        (door-location ?door ?loc)
                      )
        :effect (and
                    (not (door-state ?door closed))
                    (door-state ?door open)
                )
    )

    (:action close_door
        :parameters (?door - door ?loc - location)
        :precondition (and
                        (at-robot ?loc)
                        (door-state ?door open)
                        (door-location ?door ?loc)
                      )
        :effect (and
                    (not (door-state ?door open))
                    (door-state ?door closed)
                )
    )

    (:action open_container
        :parameters (?container - container ?tool - object)
        :precondition (and
                        (holding ?tool)
                        (container-state ?container closed)
                        (can-open ?tool ?container)
                      )
        :effect (and
                    (not (container-state ?container closed))
                    (container-state ?container open)
                )
    )

    (:action close_container
        :parameters (?container - container)
        :precondition (container-state ?container open)
        :effect (and
                    (not (container-state ?container open))
                    (container-state ?container closed)
                )
    )
    (:action pick
        :parameters (?obj - object ?loc - location ?door - door)
        :precondition (and
                        (at-robot ?loc)
                        (at ?obj ?loc)
                        (or (not (door-location ?door ?loc))
                            (and (door-location ?door ?loc)
                                (door-state ?door open)))
                        (hand-empty)
                    )
        :effect (and
                    (holding ?obj)
                    (not (at ?obj ?loc))
                    (not (hand-empty))
                )
    )

    (:action place
        :parameters (?obj - object ?loc - location ?door - door)
        :precondition (and
                        (holding ?obj)
                        (at-robot ?loc)
                       	(or (not (door-location ?door ?loc))
                            (and (door-location ?door ?loc)
                                (door-state ?door open)))
                      )
        :effect (and
                    (not (holding ?obj))
                    (at ?obj ?loc)
                    (hand-empty)
                )
    )

    (:action pour
        :parameters (?from - container ?to - container)
        :precondition (and
                        (holding ?from)
                        (container-state ?from open)
                        (container-state ?to open)
                      )
        :effect (and
                    (empty ?from)
                    (full ?to)
                )
    )
)