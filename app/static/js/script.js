// custom html element for card
class Card extends HTMLElement {
    connectedCallback() {
        // retreiving element attributes
        const name = this.getAttribute('name') || '';
        const artist = this.getAttribute('artist') || '';
        const year = this.getAttribute('year') || '';
        const rarity = this.getAttribute('rarity') || '';
        const img = this.getAttribute('img') || '';
        const quantity = this.getAttribute('quantity') || '';

        let color = '#A9A9A9'; // defualt colour (grey)


        // setting the card theme colour based on rarity
        switch (rarity.toLowerCase()){
            case 'legendary':
                color = '#E1A158';
                break;
            
            case 'epic':
                color = '#AA64E1';
                break;
            
            case 'rare':
                color = '#669DEE';
                break;

            case 'common':
                color = '#8AD97D';
                break;
        }

        // quantity bubble
        let quantityBubble = '';

        if (quantity >= 2) {
            quantityBubble = `
                <div class="quantity">
                    <span> ${quantity} </span>
                </div>
            `;
        }

        // card initialisation
        this.innerHTML = `
            <div class="card-design ${rarity.toLowerCase()}" style="box-shadow: 0 1px 8px 0px ${color}83">
                ${quantityBubble}
                <div class="rarity" style="border: 1px solid ${color}"> 
                    <div class="rarity-container" style="background-color: ${color}">${rarity.toUpperCase()}</div>
                    <svg height="100%" viewBox="0 0 30 30" fill="${color}" xmlns="http://www.w3.org/2000/svg">
                        <path d="M-0.00830078 30.4883H29.9917L-0.00830078 0.488281V30.4883Z"/>
                    </svg>           
                </div>
                <img src="${img}">
                <span class="card-name">${name}</span>
                <div class="card-details">
                    <span class="card-artist">${artist}</span>
                    <span class="card-year">${year}</span>
                </div>     
            </div>
        `;
    }
}

customElements.define('custom-card', Card);