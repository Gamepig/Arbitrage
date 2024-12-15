/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("@nomiclabs/hardhat-truffle5");
require("hardhat-tracer");
module.exports = {
    solidity: "0.6.12",
    networks: {
        // localhost: {
        //     url: "http://127.0.0.1:8545"
        // },
        hardhat: {
            chainId: 137,
            // throwOnTransactionFailures: false,
            // throwOnCallFailures: false,
            blockGasLimit: 0xFFFFFFFFFFFF,
            allowUnlimitedContractSize: true,
            forking: {
                // url: "https://polygon-mainnet.g.alchemy.com/v2/JOGYiBYYVqQJUCF1UsNqcPWNhJixWaLO",
                url: "https://polygon-rpc.com/",

            },
            mining: {
                auto: false,
                interval: 5000
            },
            accounts: {
                mnemonic: "admit good language endorse mule second blossom assume chat acid agent glance",
                count: 20
            }
        }
    }
};