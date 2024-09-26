import streamlit as st
import sounddevice as sd
import numpy as np
import plotly.graph_objects as go

# Function to update the frequency spectrum plot
def update_plot(data, sampling_rate: int, min_hz: int, max_hz: int):
    fft_result = np.fft.fft(data[:, 0])
    freqs = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)

    low_freq_indices = (freqs >= min_hz) & (freqs <= max_hz)
    low_freq_fft = fft_result[low_freq_indices]
    low_freq_freqs = freqs[low_freq_indices]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=low_freq_freqs,
        y=np.abs(low_freq_fft),
        mode='lines',
        name='Frequency Spectrum'
    ))

    fig.update_layout(
        title='Frequency Spectrum',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Amplitude'
    )

    st.plotly_chart(fig)
    

def update_waveform_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(data)),
        y=data[:, 0],
        mode='lines',
        name='Waveform'
    ))

    fig.update_layout(
        title='Waveform of Recorded Audio',
        xaxis_title='Sample',
        yaxis_title='Amplitude'
    )

    event = st.plotly_chart(fig, on_select='rerun', selection_mode='box')
    
    return event

@st.fragment()
def view(data, sampling_rate: int, min_hz: int, max_hz: int):
    with st.expander('View data'):
        st.write(data)
            
    v1, v2 = st.columns(2)
    with v1:
        event = update_waveform_plot(data=data)
               
        if event.selection.box != []: 
            start = int(min(event.selection.box[0]['x']))
            end = int(max(event.selection.box[0]['x']))
            data = data[start:end]
        
        
    with v2:
        update_plot(data, sampling_rate, min_hz=min_hz, max_hz=max_hz)


st.set_page_config('Frequency Visualizer', layout='wide')

st.title("Real-time Audio Frequency Visualization")

def main():
    
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        sampling_rate = st.radio('Sampling Rate', options=[44100, 96000], index=0, horizontal=True)
    with c2:
        duration = st.number_input('Record Duration (sec)', min_value=10, max_value=360, value=10, step=10)
    with c3:
        min_hz = st.number_input('Min Frequency (hz)', min_value=0, max_value=2000, value=0, step=100)
    with c4:
        max_hz = st.number_input('Max Frequency (hz)', min_value=0, max_value=2000, value=100, step=100)

    data = None
    if st.button('Start', use_container_width=True):
        with st.spinner("Recording audio..."):
            data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1)
            sd.wait()
            
        
            
    if data is not None:
        view(data=data, sampling_rate=sampling_rate, min_hz=min_hz, max_hz=max_hz)
    
    
if __name__ == '__main__':
    main()
