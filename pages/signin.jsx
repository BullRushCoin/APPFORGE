import { useAccount, useConnect, useSignMessage, useDisconnect } from 'wagmi';
import { InjectedConnector } from 'wagmi/connectors/injected';
import { WalletConnectConnector } from 'wagmi/connectors/walletConnect'; // Import WalletConnectConnector
import axios from 'axios';

function SignIn() {
    const { connectAsync } = useConnect();
    const { disconnectAsync } = useDisconnect();
    const { isConnected } = useAccount();
    const { signMessageAsync } = useSignMessage();

    const handleAuth = async () => {
        // Disconnects the Web3 provider if it's already active
        if (isConnected) {
            await disconnectAsync();
        }
        // Enabling WalletConnect
        const { account, chain } = await connectAsync({
            connector: new WalletConnectConnector({
                options: {
                    qrcode: true,
                },
            }),
        });

        const userData = { address: account, chain: chain.id, network: 'evm' };
        // Making a post request to our 'request-message' endpoint
        const { data } = await axios.post('/api/auth/request-message', userData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const message = data.message;
        const signature = await signMessageAsync({ message });

        console.log(signature);
    };

    return (
        <div>
            <h3>Web3 Authentication</h3>
            <button onClick={handleAuth}>Authenticate via WalletConnect</button>
        </div>
    );
}

export default SignIn;