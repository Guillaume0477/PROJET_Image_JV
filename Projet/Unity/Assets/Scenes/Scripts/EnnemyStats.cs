using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class EnnemyStats : MonoBehaviour 
{
	public EnnemyAI ennemyAI;

    private float ennemyHealth = 100;
	private Animator anim;
	private bool isTouched;

	void Start()
	{
		anim = GetComponent<Animator>();
	}
	
	void OnTriggerEnter (Collider col)
	{
        if(col.gameObject.tag == "Boule")
		{
			StartCoroutine("TakeDamageAnim");
            ennemyHealth -= 0;
			Destroy(col.gameObject);
        }
    }

	IEnumerator TakeDamageAnim()
	{
		if(!ennemyAI.getIsDead())
		{
			isTouched = true;
			anim.Play("Base Layer.Take Damage");
			yield return new WaitForSeconds(0.5f);
			isTouched = false;
		}
	}

	public float getHealth ()
	{
		return(ennemyHealth);
    }

	public bool getIsTouched ()
	{
		return(isTouched);
    }
}