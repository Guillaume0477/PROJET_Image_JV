using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyStats : MonoBehaviour 
{
    private float ennemyHealth = 100;
	private Animator anim;

	void Start()
	{
		anim = GetComponent<Animator>();
	}
	
	void OnCollisionEnter (Collision col)
	{
        if(col.gameObject.tag == "Boule"){
			anim.Play("Base Layer.Take Damage");
            ennemyHealth -= 0;
			Destroy(col.gameObject);
        }
    }

	public float getHealth ()
	{
		return(ennemyHealth);
    }
}