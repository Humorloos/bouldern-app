import numpy as np

# -1 in boundaries means maximum value for x/y-dimension of image
gyms = {
    'Studio Bloc': {
        'form_id': '1hz8f7__kzXCkZ7kOOfCHS4Kvfx4IC-nEixxIr_JvfP8',
        'sheet_id': '1OlM81rKZBlqCAVAemjsnDK0_YuJ_ykHQ-NybkzPr_aM',
        'gid': '1830339156',
        'font_size': 6,
        'sections': {
            'Q1': {
                'boundaries': np.array([[447, 96], [705, 405]]),
                'walls': []
            },
            'Q2': {
                'boundaries': np.array([[161, 0], [424, 181]]),
                'walls': [[258, 92]]
            },
            'Q3': {
                'boundaries': np.array([[139, 204], [424, 404]]),
                'walls': [
                    [247, 343],
                    [372, 343],
                    [193, 262],
                ]
            },
            'Q4': {
                'boundaries': np.array([[171, 428], [424, -1]]),
                'walls': [
                    [309, 661],
                    [360, 659],
                    [232, 620],
                ]
            },
            'Q5': {
                'boundaries': np.array([[447, 428], [-1, -1]]),
                'walls': [
                    [628, 665],
                    [588, 533],
                ]
            }
        }
    },
    'Boulder Island': {
        'form_id': '1EvUP1ubU7ftcI-OdJNxD7ypCcHNkg1_5upXQTMIQtIw',
        'sheet_id': '13OkSrXIaBmNzQCj17V2VjFXSPUe9rPHB_rmhwPfk6bk',
        'gid': '509309612',
        'font_size': 5,
        'sections': {
            'Almenhof': {
                'boundaries': np.array([[306, 1028], [589, 2058]]),
                'walls': [
                    [379, 1982],
                    [528, 1176],
                ]
            },
            'Quadrate': {
                'boundaries': np.array([[625, 1125], [907, 1615]]),
                'walls': [
                    [681, 1557]
                ]
            },
            'Herzogenried': {
                'boundaries': np.array([[965, 542], [1306, 889]]),
                'walls': [
                    [1243, 751]
                ]
            },
            'Käfertal': {
                'boundaries': np.array([[1094, 280], [1306, 629]]),
                'walls': [
                    [1145, 546],
                    [1145, 455],
                ]
            },
            'Feudenheim': {
                'boundaries': np.array([[625, 280], [1125, 463]]),
                'walls': [
                    [765, 341]
                ]
            },
            'Wallstadt': {
                'boundaries': np.array([[527, 0], [1657, 239]]),
                'walls': [
                    [921, 98]
                ]
            },
            'Gartenstadt': {
                'boundaries': np.array([[1417, 584], [-1, 1020]]),
                'walls': [
                    [1473, 635]
                ]
            },
        }
    }
}
