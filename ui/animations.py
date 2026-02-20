def fade_in(window):
    window.attributes("-alpha", 0)
    for i in range(0, 100):
        window.attributes("-alpha", i/100)
        window.update()