# hackHarvard2022

Link to video presentation - https://drive.google.com/file/d/1zgArxPzYwmf62a5V845VKVdJ5HAEgn4n/view?usp=sharing \
Link to Devpost - https://devpost.com/software/realive
Link to PPT - https://docs.google.com/presentation/d/1C7Kio21tNKrou9_KYsCsJFrpCFdYBvDT/edit?usp=sharing&ouid=117424272263224212691&rtpof=true&sd=true

Inspiration
Our inspiration has and will always be to empower various communities with tech. In this project, we attempted to build a product that can by used by anyone and everyone to have some fun with their old photos and experience them differently, using mainly auditory sense. Imagine you had an old photo of your backyard from when you were 5 but you don't remember what it sounded like back then, that's a feeling we are trying to bring back and inject some life into your photos.

What it does
The project ReAlive adds realistic sounding audio to any photo you want, trying to recreate what it would have been like back at the time of the photo. We take image as an input and return a video that is basically the same image and an audio overalyed. Now this audio is smartly synthesized by extracting information from your image and creating a mapping with our sound dataset.

How we built it
Our project is a web-app built using Flask, FastAPI and basic CSS. It provides a simple input for an image and displays the video after processing it on our backend. Our backend tech-stack is Tensorflow, Pytorch and Pydub to mix audio, with the audio data sitting on Google Cloud storage and Deep Learning models deployed on Google Cloud in containers. Our first task was to extract information from the image and then create a key-map with our sound dataset. Past that we smartly mixed the various audio files into one to make it sound realistic and paint a complete picture of the scene.

Challenges we ran into
Firstly, figuring out the depth and distance calculation for monochannel images using CNN and OpenCV was a challengin task. Next, applying this to sound intensity mapping ran us into few challenges. And finally, deploying and API latency was a factor we had to deal with and optimize.

Accomplishments that we're proud of
Building and finishing the project in 36 hours!!!

What we learned
We learned that building proof-of-concepts in two days is a really uphill task. A lot of things went our way but some didn’t, we made it at the end and our key learnings were: Creating a refreshing experience for a user takes a lot of research and having insufficient data is not great

What's next for ReAlive
Image animation and fluidity with augmented sound and augmented reality.
