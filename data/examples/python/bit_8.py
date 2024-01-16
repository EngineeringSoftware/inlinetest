from inline import itest

def find_archi(self, target_patch_size, max_layers=9):
    """
    Find the best configuration of layers using only 3x3 convs for target patch size
    """
    s = {}
    for layers_count in range(1, max_layers + 1):
        val = 1 << (layers_count - 1)
        while True:
            val -= 1

            layers = []
            sum_st = 0
            layers.append([3, 2])
            sum_st += 2
            for i in range(layers_count - 1):
                st = 1 + (1 if val & (1 << i) != 0 else 0)
                itest().given(val, 3).given(i, 0).check_eq(st, 2)
                layers.append([3, st])
                sum_st += st

            rf = self.calc_receptive_field_size(layers)

            s_rf = s.get(rf, None)
            if s_rf is None:
                s[rf] = (layers_count, sum_st, layers)
            else:
                if layers_count < s_rf[0] or (
                    layers_count == s_rf[0] and sum_st > s_rf[1]
                ):
                    s[rf] = (layers_count, sum_st, layers)

            if val == 0:
                break

    x = sorted(list(s.keys()))
    q = x[np.abs(np.array(x) - target_patch_size).argmin()]
    return s[q][2]
