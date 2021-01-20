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

	Thread receiveThread; //1
	public UdpClient client; //2
	int port; //3

	public PlayerController Player; //4
	AudioSource jumpSound; //5
	bool jump; //6
	bool fire2;
	bool Initial = true;
	bool Shield = false; //2 
	bool FireBall = false;
	bool WaveShock = false; //2 
	bool SetUpBombe = false;
	bool ActiveBombe = false;


	// 2. Initialize variables

	void Start () 
	{
	port = 5065; //1 
	Initial = true;
	Shield = false; //2 
	FireBall = false;
	WaveShock = false; //2 
	SetUpBombe = false;
	ActiveBombe = false;

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

		string Signe = Encoding.UTF8.GetString(data); //5
		if (Signe == "Signe_0!"){
			print (">> " + Signe);
			print("Position Initiale");
			Initial = true;
		}
		if (Signe == "Signe_1!"){
			print (">> " + Signe);
			Shield = true;
			Initial = false;
		}
		if (Signe == "Signe_2!"){
			print (">> " + Signe);
			SetUpBombe = true;
			Initial = false;

		}
		if (Signe == "Signe_3!"){
			print (">> " + Signe);
			FireBall = true;
			Initial = false;
		}
		if (Signe == "Signe_4!"){
			print (">> " + Signe);
			WaveShock = true;
			Initial = false;
		}
		if (Signe == "FIRE!"){
			print (">> " + Signe);
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

	if(Initial == true){
		if (Shield==true){
			print (">> " + "desactive shield");
			Player.release_shield();
			Shield=false;
		}
		if (WaveShock==true){
			print (">> " + "release wave_shock");
			Player.release_wave_shock();
			WaveShock=false;
		}
		if (SetUpBombe==true){
			print (">> " + "active bombe");
			//active bombe
			SetUpBombe=false;
		}
	}


	if(FireBall == true){ //ok
		Fire2 ();
		print (">> " + "FIRE");
		FireBall = false;
	}

	if(WaveShock == true){ //ok
		print (">> " + "charge waveshock");
		Player.charge_wave_shock();
	}

	if(Shield == true) //ok
	{
		print (">> " + "active shield");
		Player.active_shield();
	}
	if(SetUpBombe == true)
	{
		print (">> " + "set up bombe");
		Player.set_up_bombe_if_possible();
		SetUpBombe = false;
	}
	}

}
