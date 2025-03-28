import numpy as np
import pandas as pd
import torch

from types import SimpleNamespace

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression


def load_data(file_path):
    df = pd.read_csv(file_path)
    X = df.drop(columns=['2m_temperature', 'date']).values
    y = df['2m_temperature'].values
    return X, y


from models.SegRNN import Model as SegRNN
from models.SCNN import Model as SCNN

pred_len_SegRNN = [96, 192, 336, 720]
pred_len_SCNN = [3, 24, 96, 192, 336]

config_SegRNN = SimpleNamespace(
    channel_id = 1,
    d_model = 512,
    dec_way = 'pmf',
    dropout = 0.5,
    enc_in = 18,
    pred_len = pred_len_SegRNN[0],
    revin = 1,
    rnn_type = 'gru',
    seg_len = 48,
    seq_len = 720,
)

config_SCNN = SimpleNamespace(
    cycle_len = 144,
    d_model = 8,
    e_layers = 2,
    enc_in = 21,
    kernel_size = 3,
    pred_len = pred_len_SCNN[2],
    seq_len = 432,
    short_period_len = 12,
    task_name = 'long_term_forecast',
)


class SegRNNWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, input_size, hidden_size=128, output_size=1, num_layers=2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        
        self.model = SegRNN(config_SegRNN)
        self.criterion = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
    
    def fit(self, X, y, epochs=50, batch_size=32):
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
        
        X_tensor = X_tensor.unsqueeze(2)
        
        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.model.train()
        for epoch in range(epochs):
            for batch_X, batch_y in dataloader:
                self.optimizer.zero_grad()

                batch_size, seq_len, _ = batch_X.size()
                seg_num_x = self.model.seg_num_x
                seg_len = self.model.seg_len
                
                trimmed_seq_len = (seq_len // seg_len) * seg_len
                if trimmed_seq_len == 0:
                    continue
                
                batch_X_trimmed = batch_X[:, :trimmed_seq_len, :]

                reshaped_X = batch_X_trimmed.reshape(batch_size, seg_num_x, seg_len, -1)
                
                reshaped_X = reshaped_X.view(batch_size, -1, seg_len)
                reshaped_X = reshaped_X.permute(0, 2, 1)
                
                outputs = self.model(reshaped_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
        return self
    
    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X, dtype=torch.float32)

            batch_size, seq_len, _ = X_tensor.size()
            seg_num_x = self.model.seg_num_x
            seg_len = self.model.seg_len

            trimmed_seq_len = (seq_len // seg_len) * seg_len
            if trimmed_seq_len == 0:
                return np.zeros(batch_size)

            X_tensor_trimmed = X_tensor[:, :trimmed_seq_len, :]

            reshaped_X = X_tensor_trimmed.reshape(batch_size, seg_num_x, seg_len, -1)

            reshaped_X = reshaped_X.view(batch_size, -1, seg_len)
            reshaped_X = reshaped_X.permute(0, 2, 1)
            
            predictions = self.model(reshaped_X).numpy()
        return predictions.flatten()


class SCNNWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, input_size, hidden_size=128, output_size=1, num_layers=2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        
        self.model = SCNN(config_SCNN)
        self.criterion = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
    
    def fit(self, X, y, epochs=50, batch_size=32):
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.model.train()
        for epoch in range(epochs):
            for batch_X, batch_y in dataloader:
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
        return self
    
    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.tensor(X, dtype=torch.float32)
            predictions = self.model(X_tensor).numpy()
        return predictions.flatten()


def create_stacked_regressor(input_size):
    base_models = [
        ('segrnn', SegRNNWrapper(input_size=input_size)),
        ('scnn', SCNNWrapper(input_size=input_size))
    ]
    meta_model = LinearRegression()
    return StackingRegressor(estimators=base_models, final_estimator=meta_model)


if __name__ == "__main__":
    file_path = "dataset/weather.csv"
    X, y = load_data(file_path)
    input_size = X.shape[1]
    
    stacked_regressor = create_stacked_regressor(input_size=input_size)
    stacked_regressor.fit(X, y)
    
    predictions = stacked_regressor.predict(X)
    print("Predictions:", predictions)