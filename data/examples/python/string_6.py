from inline import itest

LABELS_FILENAME = "labels.txt"

def read_label_file(dataset_dir, filename=LABELS_FILENAME):
    """Reads the labels file and returns a mapping from ID to class name.

    Args:
      dataset_dir: The directory in which the labels file is found.
      filename: The filename where the class names are written.

    Returns:
      A map from a label (integer) to class name.
    """
    labels_filename = os.path.join(dataset_dir, filename)
    with tf.gfile.Open(labels_filename, "rb") as f:
        lines = f.read().decode()
    lines = lines.split("\n")
    lines = filter(None, lines)

    labels_to_class_names = {}
    for line in lines:
        index = line.index(":")
        labels_to_class_names[int(line[:index])] = line[index + 1 :]
        itest().given(line, "123:class1").given(index, 3).given(labels_to_class_names, {}).check_eq(int(line[:index]), 123).check_eq(line[index + 1 :], "class1")
    return labels_to_class_names
