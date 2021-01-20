using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class PlayerControllerScript: MonoBehaviour 
{
	// 1. Declare Variables


	// 1. Declare Variables

	Thread receiveThread; //1
	public UdpClient client; //2
	int port; //3

	public PlayerController Player; //4
	AudioSource jumpSound; //5
	bool jump; //6
	bool fire2;


	// 2. Initialize variables

	void Start () 
	{
	port = 5065; //1 
	jump = false; //2 
	fire2 = false;
	jumpSound = gameObject.GetComponent<AudioSource>(); //3

	InitUDP(); //4
	}

	// 3. InitUDP

	private void InitUDP()
	{
	print ("UDP Initialized");

	receiveThread = new Thread (new ThreadStart(ReceiveData)); //1 
	receiveThread.IsBackground = true; //2
	receiveThread.Start(); //3
	}

	// 4. Receive Data


	private void ReceiveData()
	{
	client = new UdpClient (port); //1
	while (true) //2
	{
		try
		{
		IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port); //3
		byte[] data = client.Receive(ref anyIP); //4

		//print(data);

		string text = Encoding.UTF8.GetString(data); //5
		if (text == "JUMP!"){
			print (">> " + text);
			jump = true;
		}
		if (text == "FIRE!"){
			print (">> " + text);
			fire2 = true;
		}


		 //6

		} 
		catch(Exception e)
		{
		print (e.ToString()); //7
		}
	}
	}

	// 5. Make the Player Jump

	public void Jump()
	{

	Player.fire_ball_if_possible(); //1
	//jumpSound.PlayDelayed(44100); // Play Jump Sound with a 1 second delay to match the animation
	}

	public void Fire2()
	{

	Player.fire_ball_if_possible(); //1
	//jumpSound.PlayDelayed(44100); // Play Jump Sound with a 1 second delay to match the animation
	}

	// 6. Check for variable value, and make the Player Jump!


	void Update () 
	{
	if(jump == true)
	{
		Jump ();
		jump = false;
	}
	if(fire2 == true)
	{
		Fire2 ();
		fire2 = false;
	}
	}

}
