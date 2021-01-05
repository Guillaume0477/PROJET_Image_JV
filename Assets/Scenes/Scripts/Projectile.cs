using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class Projectile : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public GameObject projectile;
	public float force;

	// At the start of the game..
	void Start ()
	{
    
    }

	// Each physics step..
	void Update ()
	{
        if (Input.GetKeyDown(KeyCode.Space)){
            GameObject balle = Instantiate(projectile, transform.position, Quaternion.identity) as GameObject;
			balle.GetComponent<Rigidbody>().velocity = transform.TransformDirection(Vector3.forward * force);
			Destroy(balle, 2.0f);
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