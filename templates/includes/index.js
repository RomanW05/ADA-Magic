/*jshint esversion: 6 */
var slider = document.getElementById("myRange");
var output = document.getElementById("mintQuantity");
output.innerHTML = slider.value; // Display the default slider value


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
    output.innerHTML = this.value;
    mintPrice.innerHTML = 'Ξ' + ethers.utils.formatEther(tokenPrice.mul(parseInt(mintQuantity.innerHTML))) + ' + gas';

};

const CONTRACT_ADDRESS = '0x6e9ce8c208393244b7adbbe09e3cbb8be1cf1034';

const NUMBER_OF_TOKENS = 5000;
let totalSupply = NUMBER_OF_TOKENS;
let supply = NUMBER_OF_TOKENS;
let tokenPrice = ethers.BigNumber.from('30000000000000000');
let provider, signer, accounts, contract, timeout;

const enableEth = document.getElementById("enableEth");
const mintBtn = document.getElementById("mintBtn");
const mintQuantity = document.getElementById("mintQuantity");
const qtyLabel = document.getElementById("qtyLabel");
const errorMsg = document.getElementById("errorMsg ");
const buyPanel = document.getElementById("buyPanel");
const showAccount = document.getElementById('showAccount');
const showTotalMinted = document.getElementById("totalSupply");
const mintPrice = document.getElementById("mintPrice");
mintPrice.innerHTML = 'Ξ' + ethers.utils.formatEther(tokenPrice.mul(parseInt(mintQuantity.innerHTML))) + ' + gas';

function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
        provider = new ethers.providers.Web3Provider(window.ethereum);
        signer = provider.getSigner();
        provider.send('eth_requestAccounts')
            .then((result) => {
                accounts = result;
                showAccount.innerHTML = accounts;

                // document.dispatchEvent(new Event('walletConnected'));
                onWalletConnected();
            })
            .catch((err) => {
                console.log("provider: " + provider);
                console.log("signer: " + signer);

                console.log(err);
                errorMsg.innerHTML = err;

            });
    } else {
        window.open('https://metamask.io/download', '_blank').focus();
    }
}

function onWalletConnected() {
    contract = new ethers.Contract(CONTRACT_ADDRESS, cryptoTunersABI, provider);
    if (ethereum.chainId != '0x1') {
        alert("You dont appear to be connected to Ethererum mainnet! Please change before continuing");
    }

    enableEth_connect();
    mintBtn.addEventListener('click', mint);

    document.dispatchEvent(new Event('fetchTotalSupply'));

    contract.on('Transfer', (from, to, tokenId, event) => {
        console.log(from, to, tokenId.toNumber());

        document.dispatchEvent(new Event('fetchTotalSupply'));
    });
}

ethereum.on('chainChanged', (chainId) => {
    // Handle the new chain.
    // Correctly handling chain changes can be complicated.
    // We recommend reloading the page unless you have good reason not to.
    window.location.reload();
});


function enableEth_connect() {
    enableEth.remove();
    buyPanel.className = "";
}

function onFetchTotalSupply() {
    contract.totalSupply()
        .then((result) => {
            totalSupply = +result;

            document.dispatchEvent(new Event('updateTotalSupply'));
        })
        .catch((err) => {
            console.log(err);

            // errorMsg.innerHTML = 'Error!  Are you connected to the correct network? (Ethereum Rinkeby)';//update to mainnet
            errorMsg.innerHTML = err;

        });

}

function onUpdateTotalSupply() {
    qtyLabel.innerHTML = NUMBER_OF_TOKENS;
    showTotalMinted.innerHTML = totalSupply + "/5000 minted";

    if (totalSupply == NUMBER_OF_TOKENS) {
        mintBtn.remove();
    }

    if (totalSupply >= NUMBER_OF_TOKENS) {
        mintBtn.remove();
    }

}


function mint() {
    let qty = parseInt(mintQuantity.innerHTML);

    let mint = NUMBER_OF_TOKENS - totalSupply;

    contract.connect(signer).mint(qty, {
            value: tokenPrice.mul(qty)
        })
        .then((result) => {
            console.log('Transaction sent successfully');
        })
        .catch((err) => {

            console.log(err);
            errorMsg.innerHTML = 'Your wallet - (' + accounts + ') does not contain enough Eth (Ξ' + ethers.utils.formatEther(tokenPrice.mul(qty)) + ') to complete this transaction';

        });

}

function onShowErrorMessage() {
    if (ethereum.chainId != '0x1') {
        errorMsg.innerHTML = 'Error!  Are you connected to the correct network? (Ethereum Mainnet)';
    }
}

enableEth.addEventListener('click', connectWallet);

// document.addEventListener('walletConnected', onWalletConnected);
document.addEventListener('fetchTotalSupply', onFetchTotalSupply);
document.addEventListener('updateTotalSupply', onUpdateTotalSupply);
document.addEventListener('showErrorMessage', onShowErrorMessage);