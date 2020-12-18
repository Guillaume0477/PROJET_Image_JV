using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerController : MonoBehaviour {
	
	// Create public variables for player speed, and for the Text UI game objects
	public float speed;

	// Create private references to the rigidbody component on the player, and the count of pick up objects picked up so far
	private Rigidbody rb_player;
	private Rigidbody ennemy_cube1_rb;
	private GameObject ennemy_cube1;

	// At the start of the game..
	void Start ()
	{
		// Assign the Rigidbody component to our private rb variable
		rb_player = GetComponent<Rigidbody>();

        //Ennemy cubes creation
        ennemy_cube1 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        Vector3 ennemy_cube1_position_initiale = new Vector3(-23.20401f, 0.5124857f, -23.86554f);
        ennemy_cube1.transform.position = ennemy_cube1_position_initiale;
		ennemy_cube1_rb = ennemy_cube1.AddComponent<Rigidbody>();
	}

	// Each physics step..
	void FixedUpdate ()
	{
        //Make the RB moving with Z Q S D
		// Set some local float variables equal to the value of our Horizontal and Vertical Inputs
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");
		// Create a Vector3 variable, and assign X and Z to feature our horizontal and vertical float variables above
		Vector3 movement = new Vector3 (moveHorizontal, 0.0f, moveVertical);
		// Add a physical force to our Player rigidbody using our 'movement' Vector3 above, 
		// multiplying it by 'speed' - our public player speed that appears in the inspector
		rb_player.AddForce (movement * speed);

        //The ennemies follow the player
        ennemy_cube1.transform.localPosition = Vector3.MoveTowards(ennemy_cube1.transform.localPosition, rb_player.position, (speed * Time.deltaTime)/3.0f);
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