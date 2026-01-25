<?php
require_once 'db.php';

function filter($data)
{
    $bad_words = ["union", "select", "from", "where", "order", "by", "limit", "group", "concat", "table", "schema", "column", "flag", " ", "\-\-", "#"];
    foreach ($bad_words as $word) {
        $data = preg_replace("/$word/i", "", $data);
    }
    return $data;
}

$title = isset($_GET['title']) ? filter($_GET['title']) : '';
$director = isset($_GET['director']) ? filter($_GET['director']) : '';
$results = [];

if ($title !== '' || $director !== '') {
    $query = "SELECT * FROM movies WHERE title LIKE '%$title%' OR director LIKE '%$director%'";
    $result = mysqli_query($conn, $query);
    if ($result) {
        $results = mysqli_fetch_all($result, MYSQLI_ASSOC);
    }
} else {
    $query = "SELECT * FROM movies LIMIT 6";
    $result = mysqli_query($conn, $query);
    if ($result) {
        $results = mysqli_fetch_all($result, MYSQLI_ASSOC);
    }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LK21 | Discover Your Next Favorite Movie</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 4rem;
        }

        h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.05em;
        }

        .search-container {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
            align-items: stretch;
        }

        .input-group {
            flex: 1;
            min-width: 280px;
            position: relative;
        }

        .search-input {
            width: 100%;
            padding: 1.2rem 1.5rem;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 1rem;
            color: white;
            font-size: 1.1rem;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }

        .search-button {
            background: var(--primary);
            border: none;
            padding: 0 1.5rem;
            border-radius: 1rem;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .search-button:hover {
            background: var(--primary-hover);
        }

        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .movie-card {
            background: var(--card-bg);
            border-radius: 1.5rem;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            backdrop-filter: blur(8px);
        }

        .movie-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 30px -10px rgba(0, 0, 0, 0.4), 0 0 15px rgba(99, 102, 241, 0.2);
            border-color: rgba(99, 102, 241, 0.5);
        }

        .poster-container {
            height: 400px;
            overflow: hidden;
            position: relative;
        }

        .poster-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .movie-card:hover img {
            transform: scale(1.05);
        }

        .movie-info {
            padding: 1.5rem;
        }

        .movie-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .movie-meta {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 1rem;
            display: flex;
            gap: 1rem;
        }

        .movie-description {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .no-results {
            text-align: center;
            grid-column: 1 / -1;
            padding: 4rem;
            color: var(--text-muted);
        }

        footer {
            margin-top: 6rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            border-top: 1px solid var(--glass-border);
            padding-top: 2rem;
        }

        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .movie-card {
            animation: fadeIn 0.6s ease forwards;
        }
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>LkSearch</h1>
            <p style="color: var(--text-muted); font-size: 1.1rem;">Explore the cinematic universe</p>
        </header>

        <section class="search-section">
            <form action="" method="GET" class="search-container">
                <div class="input-group">
                    <input type=" text" name="title" class="search-input" placeholder="Movie Title..."
                        value="<?php echo htmlspecialchars($title); ?>">
                </div>
                <div class="input-group">
                    <input type=" text" name="director" class="search-input" placeholder="Director..."
                        value="<?php echo htmlspecialchars($director); ?>">
                </div>
                <button type="submit" class="search-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                </button>
            </form>
        </section>

        <main class="results-grid">
            <?php if (empty($results)): ?>
                <div class="no-results">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"
                        style="margin-bottom: 1rem; opacity: 0.5;">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        <line x1="11" y1="8" x2="11" y2="14"></line>
                        <line x1="8" y1="11" x2="14" y2="11"></line>
                    </svg>
                    <p>No movies found matching your criteria.</p>
                </div>
            <?php else: ?>
                <?php foreach ($results as $movie): ?>
                    <article class="movie-card">
                        <div class=" poster-container"> <img src="<?php echo htmlspecialchars($movie['poster_url']); ?>"
                                alt="<?php echo htmlspecialchars($movie['title']); ?> Poster">
                        </div>
                        <div class="movie-info">
                            <h2 class="movie-title"><?php echo htmlspecialchars($movie['title']); ?></h2>
                            <div class="movie-meta">
                                <span><?php echo htmlspecialchars($movie['release_year']); ?></span>
                                <span>•</span>
                                <span>
                                    <?php echo htmlspecialchars($movie['director']); ?></span>
                            </div>
                            <p class="movie-description"><?php echo htmlspecialchars($movie['description']); ?>
                            </p>
                        </div>
                    </article>
                <?php endforeach; ?>
            <?php endif; ?>
        </main>

        <footer>
            <p>&copy; 2026 LK21 CTF Challenge. No information leakage intended.</p>
        </footer>
    </div>
</body>

</html>