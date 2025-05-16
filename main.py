
import streamlit as st
import pandas as pd
import networkx as nx

st.set_page_config(page_title="Flight Route Optimizer (IDA*)", layout="centered")

st.title("✈️ Flight Route Optimizer using IDA*")
st.markdown("Created by **Ashar Bukhari** | AI Assignment 2")
st.markdown("This app helps you find the **shortest path between airports** using Iterative Deepening A* (IDA*) algorithm on real-world route data.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/routes.csv")
    df.columns = [col.strip().lower().replace("apirport", "airport") for col in df.columns]
    return df

df = load_data()

G = nx.Graph()
for _, row in df.iterrows():
    src = row["source airport"]
    dest = row["destination airport"]
    if pd.notna(src) and pd.notna(dest):
        G.add_edge(src, dest, weight=1)

airports = sorted(set(df["source airport"].dropna().unique()).union(set(df["destination airport"].dropna().unique())))

source = st.selectbox("Select Source Airport", airports)
destination = st.selectbox("Select Destination Airport", airports)

def ida_star(graph, start, goal):
    def heuristic(n1, n2):
        return 0

    def dfs(path, g, bound):
        node = path[-1]
        f = g + heuristic(node, goal)
        if f > bound:
            return f
        if node == goal:
            return path
        min_bound = float('inf')
        for neighbor in graph.neighbors(node):
            if neighbor not in path:
                t = dfs(path + [neighbor], g + graph[node][neighbor].get("weight", 1), bound)
                if isinstance(t, list):
                    return t
                if t < min_bound:
                    min_bound = t
        return min_bound

    bound = heuristic(start, goal)
    path = [start]
    while True:
        t = dfs(path, 0, bound)
        if isinstance(t, list):
            return t
        if t == float('inf'):
            return None
        bound = t

if st.button("Find Shortest Path"):
    if source == destination:
        st.warning("Source and destination cannot be the same.")
    else:
        result = ida_star(G, source, destination)
        if result:
            st.success(f"Optimal Path: {' → '.join(result)}")
            st.info(f"Total Stops: {len(result)-1}")
        else:
            st.error("No path found between the selected airports.")
