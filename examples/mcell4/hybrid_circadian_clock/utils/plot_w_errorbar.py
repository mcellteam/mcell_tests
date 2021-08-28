import matplotlib.pyplot as plt
import numpy as np


from get_peaks_bngl import load_gdat_file
from get_peaks import prepare_data


particle_D10 = {
'A_first': (0.01292041015625, 0.0009311716138931673),
'A_second': (0.07806904296875, 0.009939225324979456),
'R_first': (0.0439923828125, 0.0032844728737789768),
'R_second': (0.10175634765625, 0.01007365051712571),
#wavelengthA: (0.0651486328125, 0.009805095633254197),
#wavelengthR: (0.05776396484375, 0.009266395224267674),
#lag_time1: (0.031071972656250002, 0.0028195598082764745),
#lag_time2: (0.0236873046875, 0.009283681378756242),
}

hybrid_D10 = {
'A_first': (0.012889941406250001, 0.0008715030086692894),
'A_second': (0.08842421875, 0.00871410129969741),
'R_first': (0.04270078125, 0.00223957984098025),
'R_second': (0.1139828125, 0.00982322230639918),
#wavelengthA: (0.07553427734375, 0.008493865698930644),
#wavelengthR: (0.07128203125, 0.009523904656041067),
#lag_time1: (0.02981083984375, 0.0017704563857977686),
#lag_time2: (0.02555859375, 0.005109072716499823),
}

particle_D1000 = {
'A_first': (0.01331298828125, 0.0009399763187567205),
'A_second': (0.1074794921875, 0.010879388950910706),
'R_first': (0.04133095703125, 0.001976249165597621),
'R_second': (0.13312890625, 0.011149581232355389),
#wavelengthA: (0.09416650390625, 0.010850965923371543),
#wavelengthR: (0.09179794921875001, 0.011025809306508929),
#lag_time1: (0.028017968749999997, 0.0013102533371181049),
#lag_time2: (0.0256494140625, 0.0012868990396521307),
}

hybrid_D1000 = {
'A_first': (0.013311914062500001, 0.000892049519092794),
'A_second': (0.107695703125, 0.011775862994309704),
'R_first': (0.0413341796875, 0.0018761307990409334),
'R_second': (0.13339716796875, 0.01200956940808676),
#wavelengthA: (0.0943837890625, 0.01170519392857754),
#wavelengthR: (0.09206298828124998, 0.01183557055892894),
#lag_time1: (0.028022265625, 0.0012663755686562895),
#lag_time2: (0.02570146484375, 0.0012651999802265157),
}

nfsim = {
'A_first': (0.0133009765625, 0.0009118954422481034),
'A_second': (0.10742314453125, 0.011697155308093971),
'R_first': (0.0413306640625, 0.00199248763803441),
'R_second': (0.13313662109375002, 0.01199618449886365),
#wavelengthA: (0.09412216796875, 0.011599305048245669),
#wavelengthR: (0.09180595703125001, 0.011792659448742138),
#lag_time1: (0.0280296875, 0.0013660731729956833),
#lag_time2: (0.025713476562499997, 0.001269598663288346),
}

ssa = {
'A_first': (0.0133234375, 0.0009217993687599999),
'A_second': (0.1070228515625, 0.011053455171801792),
'R_first': (0.041262109374999995, 0.0019458530091670484),
'R_second': (0.13263349609375003, 0.011392754685309115),
#wavelengthA: 0.09369941406250001, 0.010952303044694862
#wavelengthR: 0.09137138671875, 0.011171326917322944
#lag_time1: 0.027938671875, 0.0013354291667416
#lag_time2: 0.025610644531250004, 0.0012833446856625665
}

ode = {
'A_first': (0.0131, 0),
'A_second': (0.1098, 0),
'R_first': (0.0412, 0),
'R_second': (0.1354, 0),
#wavelengthA: (0.0967, 0),
#wavelengthR: (0.09419999999999999, 0),
#lag_time1: (0.0281, 0),
#lag_time2: (0.025599999999999998, 0),
}
        
data = [
    (1, particle_D10, 'r', 'particle 1e-7'),
    (2, hybrid_D10, 'b', 'hybrid 1e-7'),
    (3, particle_D1000, 'g', 'particle 1e-5'),
    (4, hybrid_D1000, 'm', 'hybrid 1e-5'),
    (5, nfsim, 'c', 'NFSim'),
    (6, nfsim, 'y', 'SSA'),
    (7, ode, 'k', 'ODE')
]        
        

def plot_data(only_filtering = False, base_stochastic = False):
    fig, ax = plt.subplots()
    
    if only_filtering:
        plot_compression = 1
    else:
        plot_compression = 10
    
    # load base data
    if base_stochastic:
        df_ode = load_gdat_file('../nfsim/bng/nf_00001/test.gdat')
    else:
        df_ode = load_gdat_file('../ode/test.gdat')
    
    df_ode_plot = df_ode.truncate(after = 0.16)
    if only_filtering:
        ax.plot(df_ode_plot.index, df_ode_plot['A'], label='A')
        ax.plot(df_ode_plot.index, df_ode_plot['R'], label='R')

    # must use full data for filter
    df_lowpass = df_ode.copy()
    df_lowpass = prepare_data(df_lowpass, 'A')
    df_lowpass = prepare_data(df_lowpass, 'R')

    df_lowpass = df_lowpass.truncate(after = 0.16)  
    

    ax.plot(df_lowpass.index, df_lowpass['A']/plot_compression, label='A (low pass)', c = 'b')
    ax.plot(df_lowpass.index, df_lowpass['R']/plot_compression, label='R (low pass)', c = 'r')

    if not only_filtering:
        plt.legend(['A (low pass)', 'R (low pass)'])
    else:
        plt.legend(['A', 'R', 'A (low pass)', 'R (low pass)'])
    
    if not only_filtering:
            
        base = 1350/10
        step = 200/len(data)
        
        for d in data[:-1]:
            for v in ['A_first', 'A_second', 'R_first', 'R_second']:
                # example data
                x = d[1][v][0] #np.arange(0.1, 0.2, 0.05)
                xerr = d[1][v][1] 
                y = base + d[0] * step
                
                # error bar values w/ different -/+ errors that
                # also vary with the x-position
                c = 'b' if 'A' in v else 'r'
                
                ax.errorbar(x, y, xerr=xerr, fmt='|', capsize=3, c=c)
                
                plt.text(0, y-5, d[3], c='k')
        
        plt.yticks([])
        
    # lines for ode
    if not base_stochastic:
        for v in ['A_first', 'A_second', 'R_first', 'R_second']:
            c = 'b' if 'A' in v else 'r'
            plt.axvline(x=data[6][1][v][0], c=c)
        
    plt.xlabel("time [s]")
    
    if only_filtering:
        plt.ylabel("N(t)")
                
    plt.show()


if __name__ == '__main__':
    plot_data()
    
    plot_data(True)
    
    plot_data(True, True)
    
    
