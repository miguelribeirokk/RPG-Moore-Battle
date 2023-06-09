import random


def generate_moore_machine(num_states, output_file):
    states = ['S' + str(i) for i in range(1, num_states + 1)]

    initial_state = 'S1'
    transitions = []
    not_reached_states = states.copy()

    for state in states:
        for symbol in ['0', '1', '2']:
            # Dê prioridade para não alcançados
            if len(not_reached_states) > 0:
                next_state = random.choice(not_reached_states)
                not_reached_states.remove(next_state)
                transitions.append((state, symbol, next_state))
            # Caso todos os estados já tenham sido alcançados, escolha um aleatório
            else:
                next_state = random.choice(states)
                transitions.append((state, symbol, next_state))

    with open(output_file, 'w') as file:
        # Escrever os estados
        file.write("Q: " + " ".join(states) + "\n")
        # Escrever o estado inicial
        file.write("I: " + initial_state + "\n")

        # Escrever as transições
        for transition in transitions:
            current_state, input_symbol, next_state = transition
            file.write(current_state + " -> " + next_state + " | " + input_symbol + "\n")