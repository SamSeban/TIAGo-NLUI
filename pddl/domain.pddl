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
        empty full - state
    )

    (:predicates
        (at-robot ?loc - location)
        (hand-empty)
        (holding ?obj - object)
        (at ?obj - object ?loc - location)
        (location-closed ?loc - location)
        (container-state ?container - container ?state - state)
        (container-filled ?container - container ?state - state)
        (door-location ?door - door ?loc - location)
        (can-open ?tool - object ?target - object)
    )

    (:action navigate
        :parameters (?from - location ?to - location)
        :precondition (at-robot ?from)
        :effect (and
                    (not (at-robot ?from))
                    (at-robot ?to)
                )
    )

    (:action pick
        :parameters (?obj - object ?loc - location)
        :precondition (and
                        (at-robot ?loc)
                        (at ?obj ?loc)
                        (not (location-closed ?loc))
                        (hand-empty)
                    )
        :effect (and
                    (holding ?obj)
                    (not (at ?obj ?loc))
                    (not (hand-empty))
                )
    )

    (:action place
        :parameters (?obj - object ?loc - location)
        :precondition (and
                        (holding ?obj)
                        (at-robot ?loc)
                        (not (location-closed ?loc))
                      )
        :effect (and
                    (not (holding ?obj))
                    (at ?obj ?loc)
                    (hand-empty)
                )
    )


    (:action open_door
        :parameters (?door - door ?loc - location)
        :precondition (and
                        (at-robot ?loc)
                        (door-location ?door ?loc)
                        (location-closed ?loc)
                        (hand-empty)
                      )
        :effect (and
                    (not (location-closed ?loc))
                )
    )

    (:action close_door
        :parameters (?door - door ?loc - location)
        :precondition (and
                        (at-robot ?loc)
                        (door-location ?door ?loc)
                        (not (location-closed ?loc))
                        (hand-empty)
                      )
        :effect (and
                    (location-closed ?loc)
                )
    )
    (:action open_container
        :parameters (?container - container ?tool - object ?loc - location)
        :precondition (and
                        (not (location-closed ?loc))
                        (at ?container ?loc)
                        (at-robot ?loc)
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
    (:action pour
        :parameters (?from - container ?to - container ?loc - location)
        :precondition (and
                        (not (location-closed ?loc))
                        (at ?to ?loc)
                        (at-robot ?loc)
                        (holding ?from) 
                        (container-state ?from open)
                        (container-state ?to open)
                        (container-filled ?from full)
                      )
        :effect (and
                    (container-filled ?from empty)
                    (container-filled ?to full)
                )
    )
)