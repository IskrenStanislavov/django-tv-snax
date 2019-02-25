@echo off
http -f POST localhost:8000/programs/	name="Ramstein" description="Live telecast of concert" schedule="2015-01-03 16:00:00" activeTo="2015-03-17 21:33:00Z" activeFrom="2015-03-17 21:45:00Z" channel="tv7" points=100 photo="path\my_img.jpg"
