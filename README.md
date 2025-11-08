
Precinct Map of Edmonds election results
- Note all race totals are by total for Edmonds city limits; the totals for regional races will not be reflected by city-specific maps.

to view a map https://ian33.github.io/election_results/data/maps/City_Of_Edmonds_Council_Position_3_map.html


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edmonds Election Results</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2em;
        }

        .accordion {
            background: white;
            border-radius: 8px;
            margin-bottom: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .accordion-header {
            background: #2c3e50;
            color: white;
            padding: 18px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s ease;
        }

        .accordion-header:hover {
            background: #34495e;
        }

        .accordion-header.active {
            background: #3498db;
        }

        .accordion-title {
            font-size: 1.1em;
            font-weight: 600;
        }

        .accordion-icon {
            font-size: 1.2em;
            transition: transform 0.3s ease;
        }

        .accordion-icon.rotate {
            transform: rotate(180deg);
        }

        .accordion-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .accordion-content.active {
            max-height: 85vh;
        }

        .iframe-wrapper {
            padding: 10px;
        }

        iframe {
            width: 100%;
            height: 75vh;
            border: none;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>City of Edmonds Election Results</h1>
        
        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(0)">
                <span class="accordion-title">Proposition No. 1</span>
                <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
                <div class="iframe-wrapper">
                    <iframe src="https://ian33.github.io/election_results/data/maps/City_Of_Edmonds_Proposition_No._1_map.html"></iframe>
                </div>
            </div>
        </div>

        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(1)">
                <span class="accordion-title">Council Position 1</span>
                <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
                <div class="iframe-wrapper">
                    <iframe src="https://ian33.github.io/election_results/data/maps/City_Of_Edmonds_Council_Position_1_map.html"></iframe>
                </div>
            </div>
        </div>

        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(2)">
                <span class="accordion-title">Council Position 2</span>
                <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
                <div class="iframe-wrapper">
                    <iframe src="https://ian33.github.io/election_results/data/maps/City_Of_Edmonds_Council_Position_2_map.html"></iframe>
                </div>
            </div>
        </div>

        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(3)">
                <span class="accordion-title">Council Position 3</span>
                <span class="accordion-icon">▼</span>
            </div>
            <div class="accordion-content">
                <div class="iframe-wrapper">
                    <iframe src="https://ian33.github.io/election_results/data/maps/City_Of_Edmonds_Council_Position_3_map.html"></iframe>
                </div>
            </div>
        </div>
    </div>

    <script>
        function toggleAccordion(index) {
            const accordions = document.querySelectorAll('.accordion');
            const accordion = accordions[index];
            const header = accordion.querySelector('.accordion-header');
            const content = accordion.querySelector('.accordion-content');
            const icon = accordion.querySelector('.accordion-icon');
            
            const isActive = content.classList.contains('active');
            
            // Close all accordions
            document.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.accordion-header').forEach(h => h.classList.remove('active'));
            document.querySelectorAll('.accordion-icon').forEach(i => i.classList.remove('rotate'));
            
            // Open clicked accordion if it wasn't already open
            if (!isActive) {
                content.classList.add('active');
                header.classList.add('active');
                icon.classList.add('rotate');
            }
        }

        // Open first accordion by default
        toggleAccordion(0);
    </script>
</body>
</html>
