import os
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm  # For a visual progress bar

# Choose the device: use GPU if available, otherwise CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on {device}")

# Define a heuristic for batch size: 
# If using CPU, we can use (number of CPU cores * 2) as a rough default;
# otherwise, we stick with a standard GPU batch size.
if device.type == 'cpu':
    batch_size = os.cpu_count() * 2  # This heuristic can be adjusted as needed.
else:
    batch_size = 32  # A typical batch size for GPU training; adjust as needed.

print(f"Using batch size: {batch_size}")

# Assuming you have a dataset (e.g., your custom dataset or a YOLO-specific dataset)
# Replace `YourDatasetClass` with your dataset implementation.
train_dataset = YourDatasetClass(data_yaml="C:/MP/MP2-DATA-KNIFE-GUN-1/data.yaml")
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=os.cpu_count())

# Set up your model, criterion, and optimizer
model = YourModelClass().to(device)
criterion = torch.nn.CrossEntropyLoss()  # or your specific loss
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

num_epochs = 250

# Training loop with visual epoch progress using tqdm
for epoch in range(num_epochs):
    print(f"\nEpoch {epoch + 1}/{num_epochs}")
    model.train()
    running_loss = 0.0
    
    # Use tqdm to wrap the DataLoader for a progress bar per epoch.
    for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1} Progress", unit="batch"):
        inputs, targets = batch  # Adjust based on your data structure
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    avg_loss = running_loss / len(train_loader)
    print(f"Average Loss: {avg_loss:.4f}")
