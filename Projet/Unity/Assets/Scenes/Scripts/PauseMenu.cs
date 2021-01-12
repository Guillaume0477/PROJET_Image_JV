using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class PauseMenu : MonoBehaviour
{
    public string sceneToLoad;

    public void Start()
    {
        gameObject.SetActive(true);
    }
    public void GoBackToGame()
    {
        gameObject.SetActive(false);
        Time.timeScale = 1;
    }

    public void GoBackToMainMenu()
    {
        // gameObject.SetActive(false);
        SceneManager.LoadScene(sceneToLoad);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}
