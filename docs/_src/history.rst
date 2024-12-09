Release Notes
=============

0.5.2 (2024-12-09)
------------------

* Better slide copying when loop_groups are used

0.5.1 (2024-12-08)
------------------

* Bug fix: Many elements on the slides were not getting copied. This was as a
  result of introducing loop_groups feature. But the issue happened even when
  loop_groups were not used. This has been fixed now so that there is no
  regression. Using loop_groups still cause some elements to be skipped. This
  will be incrementally fixed since python-pptx does not natively support
  copying slides.

0.5.0 (2024-12-07)
------------------

* Introduced loop_groups to enable repeating some groups of slides based on an
  iterator. This is useful for generating multiple slides based on a list of
  items.
