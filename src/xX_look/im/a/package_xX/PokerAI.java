package xX_look.im.a.package_xX;

import xX_look.im.a.package_xX.client.Client;

public class PokerAI{

	static Client client;

	public static void main(String[] args) throws Exception{
		client = new Client("ws://poker-dev.wrs.club:3001");
		client.connect();
		System.out.println("Thread continues!");
		while(true){

        }
	}

}
