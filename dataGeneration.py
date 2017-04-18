import numpy as np

def dataGeneration(data_length):
    
    # generate array of random binary
    data = np.random.randint(2, size=data_length)

    # turn array into string
    data = np.array_str(data, max_line_width=2*data_length)

    # replace non-binary characters
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace(" ", "")

    with open("data.txt", "w") as f:
         f.write(data)

if __name__ == "__main__":
    dataGeneration(1000)
