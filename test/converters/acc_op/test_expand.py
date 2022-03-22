# Owner(s): ["oncall: aiacc"]

import torch
import fx2trt_oss.tracer.acc_tracer.acc_ops as acc_ops
import torch.nn as nn
from torch.testing._internal.common_fx2trt import AccTestCase
from parameterized import parameterized
from torch.testing._internal.common_utils import run_tests


class TestExpandConverter(AccTestCase):
    @parameterized.expand(
        [
            ("2d_dim", (2, 3), (2, 1)),
            ("3d_dim", (2, 3, 4), (2, 1, 1)),
            ("4d_dim", (2, 3, 4, 5), (2, 1, 1, 1)),
            ("keep_dim", (2, 3, -1, -1), (2, 1, 5, 5)),
        ]
    )
    def test_expand(self, _, sizes, init_size):
        class Expand(nn.Module):
            def forward(self, x):
                return x.expand(*sizes)

        inputs = [torch.randn(*init_size)]
        self.run_test(
            Expand(),
            inputs,
            expected_ops={acc_ops.expand},
        )

if __name__ == '__main__':
    run_tests()
