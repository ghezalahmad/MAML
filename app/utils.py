import numpy as np
from scipy.spatial import distance_matrix
import random
import numpy as np
import torch


# Force deterministic behavior in PyTorch
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False



def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)  # Choose a fixed seed for reproducibility



# Utility function
def calculate_utility(predictions, uncertainties, apriori, curiosity, weights, max_or_min, thresholds=None):
    predictions = np.array(predictions)
    uncertainties = np.array(uncertainties)
    weights = np.array(weights).reshape(1, -1)

    # Normalize predictions
    prediction_std = predictions.std(axis=0, keepdims=True).clip(min=1e-6)
    prediction_mean = predictions.mean(axis=0, keepdims=True)
    normalized_predictions = (predictions - prediction_mean) / prediction_std

    # Compute Expected Improvement (EI) for Bayesian Optimization
    expected_improvement = np.maximum(0, (predictions - prediction_mean) - uncertainties)

    # Utility = Expected Improvement + curiosity-adjusted uncertainty
    utility = expected_improvement + curiosity * uncertainties

    return utility





# Novelty calculation
def calculate_novelty(features, labeled_features):
    if labeled_features.shape[0] == 0:
        return np.zeros(features.shape[0])
    distances = distance_matrix(features, labeled_features)
    min_distances = distances.min(axis=1)
    max_distance = min_distances.max()
    novelty = min_distances / (max_distance + 1e-6)
    return novelty



def calculate_uncertainty(model, inputs, num_perturbations=50, noise_scale=0.5):
    """
    Calculate uncertainty based on input perturbations.

    Args:
        model: Trained model to predict outputs.
        inputs: Input tensor.
        num_perturbations: Number of perturbations to apply.
        noise_scale: Standard deviation of noise added to inputs.

    Returns:
        Uncertainty scores as the standard deviation of predictions.
    """
    perturbations = []
    torch.manual_seed(42)  # Ensure fixed noise generation
    for _ in range(num_perturbations):
        noise = torch.normal(0, noise_scale, size=inputs.shape)  # Fixed noise
        perturbed_input = inputs + noise
        perturbed_prediction = model(perturbed_input).detach().numpy()
        perturbations.append(perturbed_prediction)
    perturbations = np.stack(perturbations, axis=0)
    return perturbations.std(axis=0).mean(axis=1, keepdims=True)