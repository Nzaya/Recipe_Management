const searchBtn = document.getElementById('search-btn');
const mealList = document.getElementById('meal');
const mealDetailsContent = document.querySelector('.meal-details-content');
const recipeCloseBtn = document.getElementById('recipe-close-btn');
const modalOverlay = document.getElementById('modal-overlay');
// const loader = document.getElementById('loader');

// Event listeners
searchBtn.addEventListener('click', getMealList);
mealList.addEventListener('click', getRecipeDetails);
recipeCloseBtn.addEventListener('click', closeRecipeModal);
modalOverlay.addEventListener('click', closeAddRecipeModal);
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeAddRecipeModal();
});

// Get meal list that matches with the ingredients
function getMealList() {
    const searchInputElement = document.getElementById('search-input');
    const searchInputTxt = searchInputElement.value.trim().toLowerCase();
    const mealContainer = document.getElementById('meal');

    // Clear previous results except for "Add Recipe" card
    mealContainer.innerHTML = `
        <div class="meal-item add-recipe-card" onclick="openAddRecipeModal()">
            <h3>+ Add Recipe</h3>
        </div>
    `;

    const apiUrl = `/get-recipes/?search=${encodeURIComponent(searchInputTxt)}`;
    
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.recipes.length > 0) {
                data.recipes.forEach(recipe => {
                    const recipeCard = `
                        <div class="meal-item" data-id="${recipe.id}">
                            <div class="meal-img">
                                <img src="${recipe.image || '/static/images/default-recipe.jpg'}" alt="${recipe.name}">
                            </div>
                            <div class="meal-name">
                                <h3>${recipe.name}</h3>
                                <a href="#" class="recipe-btn" data-id= "${recipe.id}" onclick="getRecipeDetails(event)">Get Recipe</a>
                            </div>
                        </div>
                    `;
                    mealContainer.innerHTML += recipeCard; // Append each recipe
                });
            } else {
                mealContainer.innerHTML += `
                    <p class="notFound">No recipes found. Try another search!</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching recipes:', error);
            mealContainer.innerHTML += `
                <p class="notFound">An error occurred. Please try again later.</p>
            `;
        });
}

// Get recipe of the meal
function getRecipeDetails(e) {
    e.preventDefault();

    if (e.target.classList.contains('recipe-btn')) {
        let mealItem = e.target.parentElement.parentElement;
        const recipeId = mealItem.dataset.id;

        // Reuse the search endpoint
        const apiUrl = `/get-recipes/?search=${encodeURIComponent('')}`; // Pass an empty search to fetch all recipes

        // showLoader();

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const recipe = data.recipes.find(r => r.id == recipeId);
                    if (recipe) {
                        mealRecipeModal(recipe); // Pass the single recipe to the modal
                    } else {
                        alert('Recipe instructions not found');
                    }
                } else {
                    alert('No recipes found.');
                }
            })
            .catch(error => {
                console.error('Error fetching recipe:', error);
                alert('Failed to fetch the recipe. Please try again later.');
            })
            // .finally(hideLoader);
    }
}

// Create a modal
function mealRecipeModal(meal) {
    // meal = meal[0];

    let html = `
        <h2 class="recipe-title">${meal.name}</h2>
        <p class="recipe-category">${meal.category}</p>
        <div class="recipe-instruct">
            <h3>Instructions:</h3>
            <p>${meal.instructions}</p>
        </div>
        <div class="recipe-meal-img">
            <img src="${meal.image}" alt="">
        </div>
    `;

    mealDetailsContent.innerHTML = html;
    mealDetailsContent.parentElement.classList.add('showRecipe');
}

function openAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'flex';
    modalOverlay.style.display = 'block';
}

function closeAddRecipeModal() {
    document.getElementById('add-recipe-modal').style.display = 'none';
    modalOverlay.style.display = 'none';
}

function closeRecipeModal() {
    mealDetailsContent.parentElement.classList.remove('showRecipe');
}

function submitRecipe(event) {
    event.preventDefault();

    const recipeName = document.getElementById('recipe-name').value;
    const recipeImage = document.getElementById('recipe-image').files[0];
    const recipeCategory = document.getElementById('recipe-category').value;
    const recipeInstructions = document.getElementById('recipe-instructions').value;

    if (!recipeName || !recipeInstructions || !recipeImage) {
        alert('Please fill in all fields and upload a valid image.');
        return;
    }

    if (!recipeImage.type.startsWith('image/')) {
        alert('Please upload a valid image file.');
        return;
    }

    const formData = new FormData();
    formData.append('name', recipeName);
    formData.append('image', recipeImage);
    formData.append('category', recipeCategory);
    formData.append('instructions', recipeInstructions);

    const submitBtn = document.getElementById('submit-recipe-btn');
    submitBtn.disabled = true;
    // showLoader();

    fetch('/add-recipe/', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Recipe added successfully!');
                closeAddRecipeModal();
                getMealList(); // Refresh the meal list
            } else {
                alert('There was an error adding the recipe. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error adding recipe:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            submitBtn.disabled = false;
            // hideLoader();
        });
}

// function showLoader() {
//     loader.style.display = 'block';
// }

// function hideLoader() {
//     loader.style.display = 'none';
// }
