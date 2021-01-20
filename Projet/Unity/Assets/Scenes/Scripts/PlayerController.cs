using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour {
    public GameObject projectile;
	public PlayerStats playerStats;
	public PlayerBar healthBar;
	public PlayerBar manaBar;
	public Text manaLacking;
	public RectTransform pauseMenu;
	public RectTransform deathMenu;
	public GameObject shockWave;
	public GameObject mine;
	public GameObject shield;

	private Rigidbody rb_player;
	private GameObject balle;
	private GameObject onde;
	private float manaDecreased = 0;
	private float manaIncreased = 0.2f;
	// Create public variables for player speed, and for the Text UI game objects
	private float player_speed = 10;
	private float sensibility = 80;
	private GameObject myMine;
	private bool action;
	private bool charge;

	// At the start of the game..
	void Start ()
	{
		// Assign the Rigidbody component to our private rb variable
		rb_player = GetComponent<Rigidbody>();

		healthBar.SetMaxValue(playerStats.getHealthMax());
		manaBar.SetMaxValue(playerStats.getManaMax());
	}

	// Each physics step..
	void FixedUpdate ()
	{
		if (charge==false){
			action = true;
		}		
		
		if(playerStats.getHealth() == 0)
		{
			healthBar.SetValue(0);
			Dead();
		}
		else
		{
			healthBar.SetValue(playerStats.getHealth());
			player_movement();
			
			if (Input.GetKeyDown(KeyCode.Escape))
			{
				pauseMenu.gameObject.SetActive(true);
				Time.timeScale = 0.0f;
			}

			if (Input.GetKeyDown(KeyCode.Space))
			{
				fire_ball_if_possible();
			}

			if (Input.GetKeyUp(KeyCode.E))
			{
				set_up_bombe_if_possible();
			
			}

			if (Input.GetKey(KeyCode.C))
			{
				charge_wave_shock();
			}

			if (Input.GetKeyUp(KeyCode.C))
			{
				release_wave_shock();
			}

			if (Input.GetKey(KeyCode.X))
			{
				active_shield();
			}

			if (Input.GetKeyUp(KeyCode.X))
			{
				release_shield();
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

	public void fire_ball_if_possible()
	{
		if(playerStats.getMana() >= projectile.GetComponent<FireBall>().getEnnemyDamage())
		{
			fire_ball();
		}
		else
		{
			manaLacking.enabled = true;
		}
	}
	
	public void set_up_bombe_if_possible()
	{

		if(mine.GetComponent<Mine>().getManaNeeded() < playerStats.getMana())
		{
			myMine = Instantiate(mine, transform.position, Quaternion.identity) as GameObject;
			myMine.transform.position = new Vector3(transform.position.x, transform.position.y - (myMine.transform.localScale.y)/2.0f, transform.position.z);
			playerStats.ApplyMana(myMine.GetComponent<Mine>().getManaNeeded());
		}
		else
		{
			manaLacking.enabled = true;
		}
	}

	public void charge_wave_shock()
	{
		if (playerStats.getMana() >= 0.5){
			playerStats.ApplyMana(0.5f);
			manaDecreased += 0.5f;
		}
		action = false;
		charge = true;
	}

	public void active_shield()
	{
		if (playerStats.getMana() >= 0.5){
			playerStats.ApplyMana(0.5f);
			manaDecreased += 0.5f;
			shield.SetActive(true) ;
			action = false;
			charge = true;
		}
		else{
			shield.SetActive(false) ;
			charge = false;
		}
	}

	public void release_shield()
	{
		shield.SetActive(false) ;
		charge = false;
	}

	public void release_wave_shock()
	{
		onde = Instantiate(shockWave, transform.position, Quaternion.identity) as GameObject;
		onde.transform.position = transform.position;
		onde.GetComponent<ShockWave>().setEnnemyDamage(manaDecreased);
		manaDecreased = 0.0f;

		charge = false;
	}
	void fire_ball()
	{
		balle = Instantiate(projectile, transform.position, Quaternion.identity) as GameObject;
		balle.GetComponent<Rigidbody>().velocity = transform.TransformDirection(Vector3.forward * balle.GetComponent<FireBall>().getForce());

		Destroy(balle, 1.0f);
		playerStats.ApplyMana(balle.GetComponent<FireBall>().getEnnemyDamage());
	}

	void Dead ()
	{
        deathMenu.gameObject.SetActive(true);
		Time.timeScale = 0;
	}

	void OnCollisionEnter(Collision col){
		if (col.gameObject.tag == "Mine"){
			playerStats.ApplyDammage(col.gameObject.transform.parent.GetComponent<Mine>().getEnnemyDamage());
		}
	}
}