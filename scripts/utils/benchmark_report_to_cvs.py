import sys    

def process_benchmark_report():
    
    while True:
        try:
            line = input()
            if line.startswith('***'):
                name = line.replace(' ', '').replace('*', '')
                print(name + ';', end='')
            elif line.startswith('Simulation'):
                time = line.split()[7]
                print(time)
            
        except EOFError:
            # no more information
            break

if __name__ == '__main__':
    process_benchmark_report()

