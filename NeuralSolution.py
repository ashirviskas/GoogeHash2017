import numpy as np
import keras
from keras.layers import *
import stuff as prb


def slices_to_map(slices, map_size, figures):
    new_map = np.zeros((map_size[0], map_size[1], len(figures) + 1), dtype=np.uint8)
    # print(new_map.nbytes)
    for s in slices:
        for i, f in enumerate(figures):
            if s.figure == f:
                new_map[s.y, s.x, i + 1] = 1
    empty_indexes = ~new_map.any(2)
    new_map[empty_indexes, 0] = 1
    return new_map

def map_to_slices(new_map, figures):
    slices = list()
    for i, f in enumerate(figures):
        slice_indexes = np.where(new_map[:, :, i + 1] == 1)
        for j in range(len(slice_indexes[0])):
            slices.append(prb.Slice(slice_indexes[1][j], slice_indexes[0][j], f))
        # print(slice_indexes)

    return slices


def build_model(figures_n):
    input = Input(shape=(None, None, 1))
    x = Conv2D(16, (24, 24), strides=(1, 1), activation='relu', padding='same')(input)
    x = Conv2D(16, (16, 16), strides=(1, 1), activation='relu', padding='same')(x)
    x = Conv2D(figures_n + 1, (16, 16), strides=(1, 1), activation='relu', padding='same')(x)
    model = keras.models.Model(input, x)
    print(model.summary())
    return model


def convert_file_to_newmap(filename):
    y_len, x_len, min_things, max_size, map_pizza = prb.read_file(filename)
    figures = prb.GenerateFigures(min_things, max_size)  # generating figures

    map_checked = np.zeros((y_len, x_len), dtype=np.bool)  # [[0 for x in range(x_len)] for y in range(y_len)]
    slices = []
    prb.CutAllPizza(map_pizza, map_checked, min_things, slices, figures, x_len, y_len)
    new_map = slices_to_map(slices, (y_len, x_len), figures)
    # slices_test = map_to_slices(new_map, figures)

    # new_map = np.expand_dims(new_map, axis=0)
    new_map = np.expand_dims(new_map, axis=0)
    print(new_map.shape)
    print(map_pizza.shape)
    return figures, map_pizza, new_map

if __name__ == '__main__':
    figures, map_pizza, new_map = convert_file_to_newmap("medium.in")
    map_pizza = np.expand_dims(map_pizza, axis=2)
    map_pizza = np.expand_dims(map_pizza, axis=0)
    model = build_model(len(figures))
    model.compile(optimizer=keras.optimizers.Adam(lr=0.0005), loss="mse",
                        metrics=['accuracy'])
    history = model.fit(map_pizza, new_map, validation_split=0.00, callbacks=[], batch_size=1, epochs=30)
    predicted_slices = model.predict(map_pizza)
    predicted_slices = np.reshape(predicted_slices, (new_map.shape[1], new_map.shape[2], new_map.shape[3]))
    output_filename = 'test_results'
    file = open(output_filename, "w")
    file.write(str(len(predicted_slices)))
    for slice in predicted_slices:
        file.write('\n')
        file.write(str(slice))
    file.close()

