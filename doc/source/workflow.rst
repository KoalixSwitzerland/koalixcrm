*********
Workflows
*********

.. blockdiag::
   :desctable:
   :caption: Workflow

   blockdiag {
      Customer -> Contract -> Quote -> C;
      Customer [description = "browsers in each client"];
      Contract [description = "web server"];
      Quote [description = "database server"];
   }
