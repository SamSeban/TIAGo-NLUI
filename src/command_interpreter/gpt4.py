import json
from openai import OpenAI

class GPT4CommandInterpreter:
    def __init__(self):
        with open("openai-credentials.json", "r") as file:
            credentials = json.load(file)
            self.api_key = credentials["api_key"]

    def send_prompt(self,prompt):
        client = OpenAI(
            api_key=self.api_key,
        )
        response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        return response.choices[0].message.content

    @staticmethod
    def create_prompt(user_command):
        prompt_template = """
    I have a service robot with the following predefined PDDL domain for task planning:

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

    Given this domain, I need to generate a PDDL problem file for the following user command: "{}".
    Based on the provided domain and the user command, create a valid PDDL problem file for this task.
    The following notes might or might not be relevant to the user command mentionned previously, you may ignore them if they are not relevant to the problem.

    Note: What I defined as a container is any object that contains liquid, like a bottle, a can, a cup, a glass etc. What I defined as a door could be any kind of door: a fridge door, a house door, a car door. Also, note that you start at "robot_location".
    Also, if you use containers that don't need to be opened they should be initialized as container-state = open. If you're trying to open a bottle that requires an opener (beer for example), initialize the opener on the kitchen counter, and add a goal to put it back on the kitchen counter. If you use drinks, they should be initialized in the fridge, unless stated otherwise.
    IMPORTANT: Make sure you don't define the same objects twice. If you use a fridge it should be defined as a location only, and you should also define a "fridge door - door" object. If you use a fridge, include a "fridge door - door", if you don't use a fridge you shouldn't include any doors.
    If include a door, initialize the door's location as location-closed, and add a goal that requires the location to be closed (meaning non accessible) in the solved state.

    Provide only the PDDL problem definition without any additional explanations or content. Start with the problem definition immediately after this instruction.
        """.format(user_command)
        return prompt_template
