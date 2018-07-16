package xX_look.im.a.package_xX.client;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.drafts.Draft_6455;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;

//this is a test
public class Client {

    WebSocketClient client;

    public Client(String uri) throws URISyntaxException{
        System.out.println("Creating Websocket connection");
        URI uriObj = new URI(uri);

        client = new WebSocketClient(uriObj, new Draft_6455()) {

            @Override
            public void onOpen(ServerHandshake serverHandshake) {
                System.out.println("Connection opened to " + uri);
                JSONObject obj = new JSONObject();
                obj.put("eventName", "__join");

                JSONObject player_info = new JSONObject();
                player_info.put("playerName", "theinterns");
                obj.put("data", player_info);
                System.out.println(obj);
                this.send(obj.toString());
            }

            @Override
            public void onMessage(String s) {
                System.out.println("Received Message from Server");
                System.out.println(s);

            }

            @Override
            public void onClose(int i, String s, boolean b) {
                System.out.println("Closed Connection");

            }

            @Override
            public void onError(Exception e) {
                System.out.println("An Error Happened");

            }
        };


    }

    public void connect(){
        client.connect();

    }
}
