import unittest
from minsait.ttaa.datio.engine.Transformer import Transformer
import pandas as pd

class TestEngine(unittest.TestCase):
    def test_add_player_cat(self):
    #    df = self.createDataFrame(data=['Guga Rodrigues', 'Gonçalo Rosa Gonçalves Pereira Rodrigues', '22', '168', '63', 'Portugal', 'Famalicão', '69', '78', 'RCM', 'A'],
    #                                    schema=['short_name', 'long_name', 'age', 'height_cm', 'weight_kg', 'nationality', 'club_name', 'overall', 'potential', 'team_position', 'player_cat'])

        dframeA = ['Guga Rodrigues', 'Gonçalo Rosa Gonçalves Pereira Rodrigues', '22', '168', '63', 'Portugal', 'Famalicão', '69', '78', 'RCM', 'A']
        dframeB = ['C. Terho','Casper Terho', '17', '180', '70', 'Finland', 'HJK Helsinki', '52', '69', 'RES', 'B']
        dframeC = ['R. Pyke', 'Rekeil Pyke', '22', '175', '65', 'England', 'Shrewsbury', '58', '67', 'ST', 'C']
        dframeD = ['D. Lovren', 'Davor Lovren', '21', '172', '70', 'Croatia', 'Fortuna Düsseldorf', '64', '76', 'SUB', 'D']
        dfA = pd.DataFrame(dframeA)
        dfB = pd.DataFrame(dframeB)
        dfC = pd.DataFrame(dframeC)
        dfD = pd.DataFrame(dframeD)

        pd.testing.assert_series_equal(Transformer.add_player_cat(self,dfA), dfA) # add assertion here



if __name__ == '__main__':
    unittest.main()
