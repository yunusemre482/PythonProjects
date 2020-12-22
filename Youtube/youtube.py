from pytube import YouTube

def download(url):
	yt=YouTube(url)
	stream=yt.streams.filter(only_audio=True).all()
	
	stream[0].download()

def  main():
	f = open("list.txt", "r")
	line=f.readline().split(',')
	for i in line:
		download(i)
	



if __name__ == "__main__":
	main()
