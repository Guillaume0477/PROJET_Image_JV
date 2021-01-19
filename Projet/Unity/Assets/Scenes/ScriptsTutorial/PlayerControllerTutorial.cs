using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class PlayerControllerTutorial : MonoBehaviour 
{
    public GameObject projectile;
	public PlayerStatsTutorial playerStats;
	public PlayerBarTutorial healthBar;
	public PlayerBarTutorial manaBar;
	public Text manaLacking;
	public RectTransform pauseMenu2;
	public GameObject shockWave;
	public GameObject mine;

	//Didacticiel
	public RectTransform Tutorial1;
	public RectTransform Tutorial2;
	public RectTransform Tutorial3;
	public RectTransform Tutorial4;
	public RectTransform Tutorial5;
	public Text count_tutorial2_text;
	public Text count_tutorial3_text;
	public Text count_tutorial4_text;
	public Text count_tutorial5_text;	

	private Rigidbody rb_player;
	private GameObject balle;
	private GameObject onde;
	private float manaDecreased = 0;
	private float manaIncreased = 0.5f;
	// Create public variables for player speed, and for the Text UI game objects
	private float player_speed = 10;
	private float sensibility = 80;
	private GameObject myMine;
	private bool AlreadyPush = false;

	static private float count_tutorial2 = 0;
	static private float count_tutorial3 = 0;
	static private float count_tutorial4 = 0;
	static private float count_tutorial5 = 0;

	// At the start of the game..
	void Start ()
	{
		// Assign the Rigidbody component to our private rb variable
		rb_player = GetComponent<Rigidbody>();

		healthBar.SetMaxValue(playerStats.getHealthMax());
		manaBar.SetMaxValue(playerStats.getManaMax());

		Tutorial1.gameObject.SetActive(true);

	}

	// Each physics step..
	void FixedUpdate ()
	{
		bool action = true;
		if(playerStats.getHealth() == 0)
		{
			healthBar.SetValue(0);
		}
		else
		{
			healthBar.SetValue(playerStats.getHealth());
			player_movement();
			
			if (Input.GetKeyDown(KeyCode.Escape))
			{
				pauseMenu2.gameObject.SetActive(true);
				Time.timeScale = 0.0f;
			}

			if(!AlreadyPush)
			{
				if(Input.GetKeyDown(KeyCode.G))
				{
					AlreadyPush = true;
					Tutorial1.gameObject.SetActive(false);
					Tutorial2.gameObject.SetActive(true);
				}
			}

			if (Input.GetKeyDown(KeyCode.Space))
			{
				if(count_tutorial2 < 3)
				{
					count_tutorial2 = count_tutorial2 + 1;
					count_tutorial2_text.text = count_tutorial2.ToString();
				}
				if(count_tutorial2 == 3)
				{
					count_tutorial2 = count_tutorial2 + 1;
					Tutorial2.gameObject.SetActive(false);
					Tutorial3.gameObject.SetActive(true);
				}
				fire_ball();
			}

			if (Input.GetKeyUp(KeyCode.E))
			{
				if(mine.GetComponent<Mine>().getManaNeeded() < playerStats.getMana())
				{
					if(count_tutorial3 < 3)
					{
						count_tutorial3 = count_tutorial3 + 1;
						count_tutorial3_text.text = count_tutorial3.ToString();
					}
					if (count_tutorial3 == 3)
					{
						count_tutorial3 = count_tutorial3 + 1;
						Tutorial3.gameObject.SetActive(false);
						Tutorial4.gameObject.SetActive(true);
					}

					myMine = Instantiate(mine, transform.position, Quaternion.identity) as GameObject;
					myMine.transform.position = new Vector3(transform.position.x, transform.position.y - (myMine.transform.localScale.y)/2.0f, transform.position.z);
					playerStats.ApplyMana(myMine.GetComponent<Mine>().getManaNeeded());
				}				
			}

			if (Input.GetKey(KeyCode.C))
			{
				if (playerStats.getManaMax() > manaDecreased){
					playerStats.ApplyMana(0.5f);
					manaDecreased += 0.5f;
				}
				action = false;
			}

			if (Input.GetKeyUp(KeyCode.C))
			{
				if(count_tutorial4 < 3)
				{
					count_tutorial4 = count_tutorial4 + 1;
					count_tutorial4_text.text = count_tutorial4.ToString();
				}
				if (count_tutorial4 == 3)
				{
					count_tutorial4 = count_tutorial4 + 1;
					Tutorial4.gameObject.SetActive(false);
					Tutorial5.gameObject.SetActive(true);
				}

				onde = Instantiate(shockWave, transform.position, Quaternion.identity) as GameObject;
				onde.transform.position = transform.position;
				onde.GetComponent<ShockWave>().setEnnemyDamage(0.0f);
				manaDecreased = 0.0f;
			}

			if(playerStats.getMana() >=  projectile.GetComponent<FireBall>().getEnnemyDamage())
			{
				manaLacking.enabled = false;
			}

			manaBar.SetValue(playerStats.getMana());
			if (action)
			{
				playerStats.RegenerateMana(manaIncreased);
			}
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
		balle.GetComponent<Rigidbody>().velocity = transform.TransformDirection(Vector3.forward * balle.GetComponent<FireBall>().getForce());

		Destroy(balle, 1.0f);
		playerStats.ApplyMana(balle.GetComponent<FireBall>().getEnnemyDamage());
	}

	void OnCollisionEnter(Collision col){
		if (col.gameObject.tag == "Mine"){
			playerStats.ApplyDammage(0.0f);
		}
	}
}