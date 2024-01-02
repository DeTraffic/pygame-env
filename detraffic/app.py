"""
FILL ME
"""

import gradio as gr
from detraffic.agent import train

demo = gr.Interface(
    fn=train,
    inputs=[gr.Number(value=30), gr.Number(value=200), gr.Number(value=1), gr.Number(value=1), gr.Number(value=1), gr.Number(value=1), gr.Slider(0, 1, value=0.6), gr.Slider(0, 1, value=0.6), gr.Slider(0, 1, value=0.6), gr.Slider(0, 1, value=0.6), gr.Slider(0, 1, value=0.05), gr.Slider(0, 1, value=0.05), gr.Slider(0, 1, value=0.05), gr.Slider(0, 1, value=0.05)],
    outputs=[]
)
demo.launch()
