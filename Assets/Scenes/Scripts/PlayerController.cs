using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerController : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
	public float player_speed;
	// public float ennemy_speed;
	public float sensibility;
    public GameObject projectile;
	public float force;

	// Create private references to the rigidbody component on the player, and the count of pick up objects picked up so far
	// private Rigidbody ennemy_cube1_rb;
	// private GameObject ennemy_cube1;
	private Rigidbody rb_player;
	private GameObject balle;
	private int count_ball = 0;
	private Collider collider;

	// At the start of the game..
	void Start ()
	{
		// Assign the Rigidbody component to our private rb variable
		rb_player = GetComponent<Rigidbody>();

        // //Ennemy cubes creation
        // ennemy_cube1 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        // Vector3 ennemy_cube1_position_initiale = new Vector3(-23.20401f, 0.5124857f, -23.86554f);
        // ennemy_cube1.transform.position = ennemy_cube1_position_initiale;
		// ennemy_cube1_rb = ennemy_cube1.AddComponent<Rigidbody>();
	}

	// Each physics step..
	void FixedUpdate ()
	{
        //Make the RB moving with Z Q S D
		// Set some local float variables equal to the value of our Horizontal and Vertical Inputs
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");

		transform.Translate(Vector3.forward * player_speed * Time.deltaTime * moveVertical);

		Vector3 YRotation = Vector3.right + new Vector3(-1.0f, 1.0f, 0.0f);
		transform.Rotate(YRotation * sensibility * Time.deltaTime * moveHorizontal);

        //The ennemies follow the player
        // ennemy_cube1.transform.localPosition = Vector3.MoveTowards(ennemy_cube1.transform.localPosition, rb_player.position, ennemy_speed * Time.deltaTime);
		
        if (Input.GetKeyDown(KeyCode.Space))
		{
			if(count_ball == 0){
				balle = Instantiate(projectile, transform.position, Quaternion.identity) as GameObject;
				balle.tag = "Boule";
				balle.GetComponent<Rigidbody>().velocity = transform.TransformDirection(Vector3.forward * force);
				
				// if(collider.gameObject.tag == "Ennemy")
				// {
				// 	Destroy(balle);
				// } else
				// {
				// 	Destroy(balle, 2.0f);
				// }
				
				count_ball = 1;
				Destroy(balle, 1.0f);
			}
			else{
				if(balle == null){
					count_ball = 0;
				}
			}
		}
	}
	
	// When this game object intersects a collider with 'is trigger' checked, 
	// store a reference to that collider in a variable named 'other'..
	void OnTriggerEnter(Collider other) 
	{
		// ..and if the game object we intersect has the tag 'Pick Up' assigned to it..
		if (other.gameObject.CompareTag ("Pick Up"))
		{
			// Make the other game object (the pick up) inactive, to make it disappear
			other.gameObject.SetActive (false);
		}
	}
}