using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour {
	// public float ennemy_speed;
    public GameObject projectile;
	public PlayerStats playerStats;
	public PlayerBar healthBar;
	public PlayerBar manaBar;
	public Text manaLacking;
	public RectTransform pauseMenu;
	public RectTransform deathMenu;

	// Create private references to the rigidbody component on the player, and the count of pick up objects picked up so far
	// private Rigidbody ennemy_cube1_rb;
	// private GameObject ennemy_cube1;
	private Rigidbody rb_player;
	private GameObject balle;
	private int count_ball = 0;
	private float manaDecreased = 30;
	private float manaIncreased = 0.1f;
	// Create public variables for player speed, and for the Text UI game objects
	private float player_speed = 10;
	private float sensibility = 80;
	private float force = 20;

	// At the start of the game..
	void Start ()
	{
		// Assign the Rigidbody component to our private rb variable
		rb_player = GetComponent<Rigidbody>();

		healthBar.SetMaxValue(playerStats.getHealthMax());
		manaBar.SetMaxValue(playerStats.getManaMax());

        // //Ennemy cubes creation
        // ennemy_cube1 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        // Vector3 ennemy_cube1_position_initiale = new Vector3(-23.20401f, 0.5124857f, -23.86554f);
        // ennemy_cube1.transform.position = ennemy_cube1_position_initiale;
		// ennemy_cube1_rb = ennemy_cube1.AddComponent<Rigidbody>();
	}

	// Each physics step..
	void FixedUpdate ()
	{
		if(playerStats.getHealth() == 0)
		{
			healthBar.SetValue(0);
			Dead();
		}
		else
		{
			healthBar.SetValue(playerStats.getHealth());
			//The ennemies follow the player
			// ennemy_cube1.transform.localPosition = Vector3.MoveTowards(ennemy_cube1.transform.localPosition, rb_player.position, ennemy_speed * Time.deltaTime);
			player_movement();
			
			if (Input.GetKeyDown(KeyCode.Escape))
			{
				pauseMenu.gameObject.SetActive(true);
				Time.timeScale = 0.0f;
			}

			if (Input.GetKeyDown(KeyCode.Space))
			{
				if(playerStats.getMana() >=  manaDecreased)
				{
					fire_ball();
				}
				else
				{
					manaLacking.enabled = true;
				}
			}

			if(playerStats.getMana() >=  manaDecreased)
			{
				manaLacking.enabled = false;
			}

			manaBar.SetValue(playerStats.getMana());
			playerStats.RegenerateMana(manaIncreased);
		}
	}
	
	void player_movement()
	{
 		//Make the RB moving with Z Q S D
		// Set some local float variables equal to the value of our Horizontal and Vertical Inputs
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");

		transform.Translate(Vector3.forward * player_speed * Time.deltaTime * moveVertical);

		Vector3 YRotation = Vector3.right + new Vector3(-1.0f, 1.0f, 0.0f);
		transform.Rotate(YRotation * sensibility * Time.deltaTime * moveHorizontal);
	}

	void fire_ball()
	{
		balle = Instantiate(projectile, transform.position, Quaternion.identity) as GameObject;
		balle.tag = "Boule";
		balle.GetComponent<Rigidbody>().velocity = transform.TransformDirection(Vector3.forward * force);

		count_ball = 1;
		Destroy(balle, 1.0f);
		playerStats.ApplyMana(manaDecreased);
	}

	void Dead ()
	{
        deathMenu.gameObject.SetActive(true);
		Time.timeScale = 0;
	}
}