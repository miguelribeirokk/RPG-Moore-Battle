import random

def generate_moore_machine(num_states, output_file):
    states = ['S' + str(i) for i in range(1, num_states + 1)]

    initial_state = 'S1'
    transitions = []
    estados_nao_alcacados = states.copy()

    for state in states:
        for symbol in ['0', '1', '2']:
            # Dê prioridade para não alcançados
            if len(estados_nao_alcacados) > 0:
                next_state = random.choice(estados_nao_alcacados)
                estados_nao_alcacados.remove(next_state)
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

# Gerar uma máquina de Moore totalmente completa com 10 estados (incluindo o estado inicial "S1") e salvar no arquivo "moore_machine.txt"
generate_moore_machine(10, "moore_machine.txt")