from matplotlib import pyplot as plt

import NuRadioReco.modules.io.eventReader
event_reader = NuRadioReco.modules.io.eventReader.eventReader()

file = 'myout.nur'
event_reader.begin(file)
for iE, event in enumerate(event_reader.run()):
    primary = event.get_primary()

    for iStation, station in enumerate(event.get_stations()):

        fig, axs = plt.subplots(4, 1, figsize=(5,20))

        # this loops through "mock data" (with noise added, etc.)
        for ch in station.iter_channels():
            volts = ch.get_trace()
            times = ch.get_times()
            axs[ch.get_id()].plot(times, volts)
        
        # this loops through *MC truth* waveforms (before noise was added)
        if station.has_sim_station():
            sim_station = station.get_sim_station()
            for sim_ch in sim_station.iter_channels():
                print(sim_ch.get_id())
                volts = sim_ch.get_trace()
                times = sim_ch.get_times()
                axs[sim_ch.get_id()].plot(times, volts, '--')

        fig.savefig(f"traces_{iE}.png")

