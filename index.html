<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meme Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
        }
        .modal-content {
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90%;
        }
        .skeleton-loader {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        @keyframes loading {
            0% {
                background-position: 200% 0;
            }
            100% {
                background-position: -200% 0;
            }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">Meme Generator</h1>

        <div class="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-md">
            <form id="memeForm" class="mb-6">
                <textarea
                    id="promptInput"
                    rows="4"
                    class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your prompt to generate memes..."
                ></textarea>
                <button
                    type="submit"
                    class="w-full mt-4 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition duration-300"
                >
                    Generate Memes
                </button>
            </form>
        </div>

        <div id="loadingSpinner" class="hidden text-center mt-8">
            <div class="spinner-border text-blue-600" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            <p class="mt-4 text-gray-600">Generating memes...</p>
        </div>

        <div id="resultsContainer" class="mt-8">
            <div id="sentimentsSection" class="mb-8">
                <h2 class="text-2xl font-semibold mb-4 text-center text-blue-600">Detected Sentiments</h2>
                <div id="sentimentsList" class="flex justify-center flex-wrap gap-2"></div>
            </div>

            <div id="mongoMemesSection" class="mb-8 hidden">
                <h2 class="text-2xl font-semibold mb-4 text-center text-blue-600">Sentiment-Based Memes</h2>
                <div id="mongoMemeGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
            </div>

            <div id="aiMemesSection" class="mb-8 hidden">
                <h2 class="text-2xl font-semibold mb-4 text-center text-blue-600">AI Generated Memes</h2>
                <div id="aiMemeGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"></div>
            </div>
        </div>
    </div>

    <!-- Modal for full image -->
    <div id="imageModal" class="modal">
        <span class="close absolute top-4 right-4 text-white text-4xl cursor-pointer">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>

    <script>
                document.getElementById('memeForm').addEventListener('submit', function(e) {
            e.preventDefault();

            // Clear previous results
            document.getElementById('sentimentsList').innerHTML = '';
            const mongoMemesSection = document.getElementById('mongoMemesSection');
            const aiMemesSection = document.getElementById('aiMemesSection');
            const mongoMemeGrid = document.getElementById('mongoMemeGrid');
            const aiMemeGrid = document.getElementById('aiMemeGrid');

            mongoMemeGrid.innerHTML = '';
            aiMemeGrid.innerHTML = '';

            mongoMemesSection.classList.add('hidden');
            aiMemesSection.classList.add('hidden');

            // Show loading spinner
            document.getElementById('loadingSpinner').classList.remove('hidden');

            const prompt = document.getElementById('promptInput').value;

            // Function to create image grid with loading and modal support
            function createImageGrid(container, section, url) {
                const imgDiv = document.createElement('div');
                imgDiv.classList.add('bg-white', 'p-2', 'rounded-lg', 'shadow-md', 'cursor-pointer', 'relative');

                // Create a skeleton loader
                const skeletonLoader = document.createElement('div');
                skeletonLoader.classList.add('skeleton-loader', 'absolute', 'inset-0', 'z-10');
                imgDiv.appendChild(skeletonLoader);

                const img = document.createElement('img');
                img.classList.add('w-full', 'h-48', 'object-cover', 'rounded', 'opacity-0', 'transition-opacity', 'duration-300');

                // Image load event
                img.onload = () => {
                    img.classList.remove('opacity-0');
                    skeletonLoader.remove();
                    section.classList.remove('hidden');
                };

                img.src = url;

                // Add click event to show full image
                img.addEventListener('click', () => {
                    const modal = document.getElementById('imageModal');
                    const modalImage = document.getElementById('modalImage');
                    modalImage.src = url;
                    modal.style.display = 'block';
                });

                imgDiv.appendChild(img);
                container.appendChild(imgDiv);
            }

            // Create EventSource for streaming
            const eventSource = new EventSource(`/process?prompt=${encodeURIComponent(prompt)}`);

            // Handle sentiments
            eventSource.addEventListener('sentiments', function(event) {
                const sentiments = JSON.parse(event.data);
                const sentimentsList = document.getElementById('sentimentsList');
                sentiments.forEach(sentiment => {
                    const span = document.createElement('span');
                    span.classList.add('bg-blue-100', 'text-blue-800', 'text-sm', 'font-medium', 'mr-2', 'px-2.5', 'py-0.5', 'rounded');
                    span.textContent = sentiment;
                    sentimentsList.appendChild(span);
                });
            });

            // Handle sentiment-based memes
            eventSource.addEventListener('sentiment_meme', function(event) {
                createImageGrid(mongoMemeGrid, mongoMemesSection, event.data);
            });

            // Handle AI-generated memes
            eventSource.addEventListener('ai_meme', function(event) {
                createImageGrid(aiMemeGrid, aiMemesSection, event.data);
            });

            // Handle completion
            eventSource.addEventListener('complete', function() {
                document.getElementById('loadingSpinner').classList.add('hidden');
                eventSource.close();
            });

            // Handle errors
            eventSource.addEventListener('error', function(error) {
                console.error('EventSource failed:', error);
                document.getElementById('loadingSpinner').classList.add('hidden');
                alert('An error occurred while generating memes.');
                eventSource.close();
            });
        });

        // Modal close functionality
        const modal = document.getElementById('imageModal');
        const closeBtn = document.querySelector('.close');

        closeBtn.onclick = () => {
            modal.style.display = 'none';
        };

        // Close modal when clicking outside the image
        window.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    </script>
</body>
</html>