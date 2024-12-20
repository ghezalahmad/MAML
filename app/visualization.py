import plotly.graph_objects as go
from sklearn.manifold import TSNE
import plotly.express as px

import pandas as pd

# Scatter plot
def plot_scatter_matrix(result_df, target_columns, utility_scores):
    scatter_data = result_df[target_columns + ["Utility"]].copy()
    scatter_data["Utility"] = utility_scores

    fig = px.scatter_matrix(
        scatter_data,
        dimensions=target_columns,
        color="Utility",
        color_continuous_scale="Viridis",
        title="Scatter Matrix of Target Properties",
        labels={col: col for col in target_columns},
    )
    fig.update_traces(diagonal_visible=False)
    return fig



def create_tsne_plot(data, features, utility_col="Utility", perplexity=20, learning_rate=200):
    """
    Create a t-SNE plot for the dataset.

    Args:
        data (pd.DataFrame): The dataset with features and utility.
        features (list): The list of feature column names.
        utility_col (str): Column name representing utility scores.
        perplexity (int): Perplexity parameter for t-SNE.
        learning_rate (int): Learning rate for t-SNE optimization.

    Returns:
        plotly.graph_objects.Figure: A scatter plot in t-SNE space.
    """
    if len(features) == 0:
        raise ValueError("No features selected for t-SNE.")

    if utility_col not in data.columns:
        raise ValueError(f"The column '{utility_col}' is not in the dataset.")

    tsne = TSNE(
        n_components=2,
        perplexity=min(perplexity, len(data) - 1),
        n_iter=350,
        random_state=42,
        init="pca",
        learning_rate=learning_rate,
    )

    # Fit t-SNE on the selected feature columns
    tsne_result = tsne.fit_transform(data[features])

    # Create a dataframe with t-SNE results
    tsne_result_df = pd.DataFrame({
        "t-SNE-1": tsne_result[:, 0],
        "t-SNE-2": tsne_result[:, 1],
        utility_col: data[utility_col].values,
    })

    # Generate scatter plot
    fig = px.scatter(
        tsne_result_df,
        x="t-SNE-1",
        y="t-SNE-2",
        color=utility_col,
        title="t-SNE Visualization of Data",
        labels={"t-SNE-1": "t-SNE Dimension 1", "t-SNE-2": "t-SNE Dimension 2"},
        color_continuous_scale="Viridis",
    )

    fig.update_traces(marker=dict(size=7))
    fig.update_layout(height=800, legend_title_text="Utility")
    return fig



def plot_histogram(data, column_name):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.hist(data[column_name], bins=20, alpha=0.75, color="blue")
    plt.title(f"Histogram of {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    st.pyplot(plt)


def plot_scatter(data, x, y, labels=None):
    fig = px.scatter(data, x=x, y=y, color=labels, title=f"{x} vs {y}")
    st.plotly_chart(fig)



import plotly.express as px

def create_parallel_coordinates(result_df, dimensions, color_column):
    """
    Create a parallel coordinate plot using Plotly.
    
    Args:
        result_df (pd.DataFrame): DataFrame containing the results.
        dimensions (list): List of column names to include as axes.
        color_column (str): Column name for coloring the lines.

    Returns:
        fig: Plotly figure for the parallel coordinate plot.
    """
    fig = px.parallel_coordinates(
        result_df,
        dimensions=dimensions,
        color=color_column,
        title="Parallel Coordinate Plot",
        labels={col: col for col in dimensions + [color_column]},
        template="plotly_white",
    )
    return fig


# Function for 3D scatter plot
import plotly.express as px

def create_3d_scatter(result_df, x_column, y_column, z_column, color_column):
    """
    Create a 3D scatter plot using Plotly with larger dimensions.
    
    Args:
        result_df (pd.DataFrame): DataFrame containing the results.
        x_column (str): Column name for the x-axis.
        y_column (str): Column name for the y-axis.
        z_column (str): Column name for the z-axis.
        color_column (str): Column name for coloring the points.

    Returns:
        fig: Plotly figure for the 3D scatter plot.
    """
    fig = px.scatter_3d(
        result_df,
        x=x_column,
        y=y_column,
        z=z_column,
        color=color_column,
        title=f"3D Scatter Plot ({x_column} vs {y_column} vs {z_column})",
        labels={x_column: x_column, y_column: y_column, z_column: z_column, color_column: color_column},
        template="plotly_white",
    )
    # Increase marker size
    fig.update_traces(marker=dict(size=8))
    # Increase the figure size
    fig.update_layout(
        scene=dict(
            xaxis_title=x_column,
            yaxis_title=y_column,
            zaxis_title=z_column,
        ),
        height=900,  # Increased height
        width=1200,   # Increased width
        margin=dict(l=0, r=0, t=50, b=0)  # Adjusted margins
    )
    return fig
