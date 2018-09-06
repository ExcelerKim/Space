def plotdata():
    import seaborn as sns
    from bokeh.embed import components
    from bokeh.plotting import figure
    data = sns.load_dataset('tips')
    data2 = data.groupby(['smoker']).mean().tip
    p = figure(x_range=['Yes', 'No'], plot_width=400, plot_height=300)
    p.vbar(x=['Yes', 'No'], bottom=2.8, width=0.5, top=data2, color="#CAB2D6")
    # p.line(df['date'], df['close'], color='navy', alpha=0.5)
    return components(p)
